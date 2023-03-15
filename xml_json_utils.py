from datetime import datetime


def get_json_data(data, extraction_list):
    temp = []
    for i in extraction_list:
        if i == "created-on" or i == "last-modified":
            try:
                _temp = datetime.fromtimestamp(int(data[i][:10]))
            except:
                _temp = ""
        
        elif i == "path":
            _temp = "https://www.zu.ac.ae/main" + data[i]
            if "/_deleted_items" in _temp or "/_hidden" in _temp or "/_older_deleted_items" in _temp:
                break
        
        elif i == "dynamic-metadata":
            _temp = ""
        
        else:
            try:
                _temp = data[i]
            
            except:
                _temp = ""
        
        temp.append(_temp)
    
    if len(temp) != 7:
        return None
    return temp


def get_xml_data(data):
    extraction_list = ["id", "path", "title", "summary", "created-on", "last-modified", "dynamic-metadata"]

    temp = []
    for i in extraction_list:
        try:
            if i == "created-on" or i == "last-modified":
                _temp = datetime.fromtimestamp(int(data.find(i).text[:10]))
            
            elif i == "path":
                _temp = "https://www.zu.ac.ae/main" + data.find(i).text
                if "/_deleted_items" in _temp or "/_hidden" in _temp or "/_older_deleted_items" in _temp:
                    break
            
            elif i == "id":
                try:
                    _temp = data.attrib['id']
                except:
                    _temp = ""
            
            elif i == "title":
                try:
                    _temp = data.find(i).text
                except:
                    _temp = data.find("name").text

            else:
                try:
                    _temp = data.find(i).text
                except:
                    _temp = ""

            temp.append(_temp)
        except:
            pass

    if len(temp) != 7:
        return None
    return temp