from xml_json_utils import get_xml_data, get_json_data
import json, os
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
import http.client
from bs4 import BeautifulSoup
import csv
from multi_config import *


def get_data(files, NEW_FILES_DIR):
    links = []
    for file in files:
        if ".xml" in file:
            root = ET.parse(os.path.join(NEW_FILES_DIR, file)).getroot()

            sys_folder = [elem for elem in root.iter("system-folder")]
            sys_file = [elem for elem in root.iter("system-file")]
            sys_page = [elem for elem in root.iter("system-page")]
            system = [sys_folder, sys_file, sys_page]

            for sys in system:
                if len(sys) > 0:
                    for folder in sys:
                        extracted_data = get_xml_data(folder)
                        if extracted_data:
                            links.append(get_xml_data(folder))

        else:
            data = json.load(open(os.path.join(NEW_FILES_DIR, file), encoding='utf-8'))

            if len(data) > 1:
                json_extract_list = ["ServiceID", "ServiceUrl", "ServiceName", "Description", "created_on", "last-modified", "dynamic-metadata"]

                for sys_data in data:
                    extracted_data = get_json_data(sys_data, json_extract_list)
                    if extracted_data:
                        links.append(extracted_data)
            
            else:
                data = data['assets']
                extraction_list = ["id", "path", "title", "description", "created-on", "last-modified", "dynamic-metadata"]

                for sys_data in data:
                    extracted_data = get_json_data(sys_data, extraction_list)
                    if extracted_data:
                        links.append(extracted_data)
    
    return links


def remove_404(process_data):
    extracted = process_data[0]
    non_404_links = process_data[1]
    
    for i in range(len(extracted)):
        try:
            is_extension_present = False
            for extension in EXTENSION_LIST:
                if extension.lower() in extracted[i][1].lower():
                    # print(i, len(extracted), extracted[i][1])
                    non_404_links.append(extracted[i])
                    is_extension_present = True
                    break
            
            if not is_extension_present:
                parsed_url = urlsplit(extracted[i][1])
                hostname = parsed_url.netloc
                conn = http.client.HTTPSConnection(hostname)
                payload = ""
                headers = {'Cookie': 'ASP.NET_SessionId=wup0uqgvslgafoin5qndwbm4'}
                _path = parsed_url.path
                if " " in parsed_url.path:
                    _path = parsed_url.path.replace(" ", "%20")

                conn.request("GET", _path, payload, headers)
                res = conn.getresponse()
                data = res.read().decode()
                soup = BeautifulSoup(data, 'html.parser')
                a_tag = soup.find('a')
                href_val = a_tag.get('href')

                if "404" in href_val or "Invalid.html" in href_val:
                    # print(i, len(extracted), "404 found in the href of the a tag", extracted[i][1])
                    pass
                
                else:
                    # print(i, len(extracted), extracted[i][1])
                    non_404_links.append(extracted[i])
        except Exception as e:
            # print(i, len(extracted), "[ERROR] EXCEPTION", extracted[i][1], e)
            pass
    
    save_file_csv = os.path.join(SAVE_FILES_DIR, SAVE_FILE_NAME)
    with open(save_file_csv, "a", encoding="utf-8", newline="\n") as fp:
        writer = csv.writer(fp)
        writer.writerows(non_404_links)
    
    return non_404_links
