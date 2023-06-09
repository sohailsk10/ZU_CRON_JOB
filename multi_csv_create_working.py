import multiprocessing
from datetime import datetime
import numpy as np
import requests, os, json, itertools, csv
from multiprocessing_utils import get_data, remove_404
from multi_config import *
import time

save_file_csv = os.path.join(NEW_FILES_DIR_SERVER, SAVE_FILE_NAME)
save_arabic_file_csv = os.path.join(NEW_FILES_DIR_SERVER, SAVE_ARABIC_FILE_NAME)

if os.path.exists(save_file_csv):
    os.remove(save_file_csv)

if not os.path.exists(NEW_FILES_DIR_SERVER):
    os.mkdir(NEW_FILES_DIR_SERVER)
else:
    files = [files for _, _, files in os.walk(NEW_FILES_DIR_SERVER)][0]
    for _file in files:
        os.remove(os.path.join(NEW_FILES_DIR_SERVER, _file))


if not os.path.exists(SAVE_FILES_DIR):
    os.mkdir(SAVE_FILES_DIR)


def get_div(data):
    rem = len(data) % NUMBER_OF_PROCESSES
    dividend = int((len(data) - rem) / NUMBER_OF_PROCESSES)
    divided_list_range = []
    for i in range(NUMBER_OF_PROCESSES):
        if i > 0:
            divided_list_range.append(((dividend*i) + 1, dividend*(i+1)))
        else:
            divided_list_range.append((i, dividend))
    
    divided_list_range[-1] = (divided_list_range[-1][0], divided_list_range[-1][1] + rem)
    print(divided_list_range)

    return divided_list_range


if __name__ == '__main__':
    if DOWNLOAD_FILES:
        for filename in FILES_TO_FETCH:
            if ".xml" in filename:
                try:
                    file_part_name = filename.split("/en/")[1].split(".")[0]
                    file_name = file_part_name + "_en.xml"
                    
                except:
                    file_part_name = filename.split("/ar/")[1].split(".")[0]
                    file_name = file_part_name + ".xml"
                
                
                response = requests.get(filename)
                with open(NEW_FILES_DIR_SERVER + file_name, 'wb') as file:
                    file.write(response.content)

                print("DOWNLOAD", file_name)
            
            else:
                file_name = filename.split("/")[-1]
                if ".json" not in file_name:
                    file_name = filename.split("/")[-1] + ".json"
                
                response = requests.get(filename)
                data = response.json()
                with open(NEW_FILES_DIR_SERVER + file_name, 'w') as f:
                    json.dump(data, f)

                print("DOWNLOAD", file_name)
    if PROCESSED_FILES:
        files = [files for _, _, files in os.walk(NEW_FILES_DIR_SERVER)][0]
        print("FILES", files)

        extracted_data = get_data(files, NEW_FILES_DIR_SERVER)
        print("LENGTH EXTRACTED DATA", len(extracted_data))
        divided_list_range = get_div(extracted_data)
        
        remove_404_parameters = [(extracted_data[div[0]:div[1] + 1], []) for div in divided_list_range]
        
        print(len(remove_404_parameters))
        print(len(remove_404_parameters[0][0]))
        print(len(remove_404_parameters[1][0]))

        remove_404_pool = multiprocessing.Pool()
        result_404 = remove_404_pool.map(remove_404, remove_404_parameters)
        
        non_404_links = list(itertools.chain.from_iterable(result_404))
        divided_list_range = get_div(non_404_links)

        print(f"WRINTING IN {save_file_csv} NON 404 LINKS")
        with open(save_file_csv, "w", newline="\n", encoding="utf-8") as save_fp:
            writer = csv.writer(save_fp)
            writer.writerow(["id", "path", "title", "description", "created-on", "last-modified", "dynamic-metadata"])
            writer.writerows(non_404_links)
        
        with open(save_file_csv, encoding='utf-8') as input_file:
            reader = csv.reader(input_file)
            with open(save_arabic_file_csv, 'w', encoding='utf-8', newline='\n') as arabic_file:
                arabic_writer = csv.writer(arabic_file)
                arabic_writer.writerow(['id','path','title','description','created-on','last-modified','dynamic-metadata'])

                for row in reader:
                    if '/ar/' in str(row[1]):
                        arabic_writer.writerow(row)

    # os.system('kill $(lsof -t -i:8000)')  # kill the Django server process
    # os.system("kill $(netstat -ano | findstr :8000 | awk '{print $5}')")  # kill the Django server process
    # os.system("taskkill /pid $(netstat -ano | findstr :8000 | awk '{print $5}')")  # kill the Django server process
    os.system("taskkill netstat -ano | for /f 'tokens=5' %a in ('findstr :8000') do @echo %a")  # kill the Django server process
    print("DJANGO SERVER STOPPED")
    time.sleep(20)  # wait for the process to be killed
    os.system('cd /home/chatbot_root/Zayed-University-Chatbot/')
    os.system('ls')
    time.sleep(10)
    os.system('nohup python3 manage.py runserver 0:8000 &')
    os.system("xdotool key Return")
    print("DJANGO SERVER STARTED")
    print("DONE")
