import os
import sys
import chardet
import shutil
import json
import datetime


appdata_dir = os.getenv('APPDATA') 
log_dir = os.path.join(appdata_dir, 'Conversie Diacritice')
log_path = os.path.join(log_dir, 'log.txt') # AppData\Roaming\Conversie Diacritice\log.txt
os.makedirs(log_dir, exist_ok=True)

def get_json_data():
    # Get the folder where the .exe is located 
    exe_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    json_path = os.path.join(exe_dir, "map.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f) 
    except (FileNotFoundError, json.JSONDecodeError):
        raise("Error: missing map.json file")
        

def get_encoding(filePath):
    with open(filePath, 'rb') as file:
        detector=chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break    
        detector.close()
    return detector.result['encoding']

def convert_to_utf8(file_path):
    # 1. Read file as binary (byte string)
    with open(file_path, 'rb') as f:
        content = f.read()
    # 2. Force decode as Latin-1 (never fails) then encode as UTF-8
    utf8_content = content.decode('latin-1').encode('utf-8')
    # 3. Write to temp file
    temp_file = file_path + '.tmp'
    with open(temp_file, 'wb') as f:
        f.write(utf8_content)
    # 4. Replace original file
    shutil.move(temp_file, file_path)

def main():
    if len(sys.argv)>1:
        file=sys.argv[1]
        # print(file)
    else:
        raise("No file provided!")
    
    # loading replacement chars
    charMap=get_json_data()
    # print(charMap)
    # charMap={
    #     "\u00ba": "s",
    #     "\u00fe": "t",
    #     "\u00aa": "S",
    #     "\u00de": "T" 
    # }

    # making file backup
    bakfile=file+".bak"
    if os.path.isfile(bakfile): open(bakfile,"w").close() # clearing file if ti already exists 
    with open(bakfile, "w") as fout:
        fout.write("")
    shutil.copyfile(file, bakfile)

    fencod=get_encoding(file)
    # read file line by line and store it into a a list
    with open(file, 'r', encoding=fencod) as f:
        lines = f.readlines()
    # print(lines)

    # converting file encoding to utf-8
    # ok maybe not
    # fencod=get_encoding(file) 
    # print(fencod)
    # if fencod!='utf-8': convert_to_utf8(file)
    # print(get_encoding(file))

    # replacing all the chars from the file with the right diacritics
    if os.path.isfile(file): open(file,"w").close()
    with open(file,"w",encoding=fencod) as _:
        for line in lines:
            str=""
            for i in range(len(line)):
                if line[i] not in charMap.keys():
                    str+=line[i]
                else: str+=charMap[line[i]]
            _.write(str)

if __name__=="__main__":
    with open(log_path, 'w') as f:
        sys.stdout = f
        try:
            main()
            now=datetime.datetime.now()
            print(f"succes ---- {now}")
        except Exception as e:
            print(e)
            sys.stdout=sys.__stdout__ 
            print("conversion failed, check log.txt to see the error")
            exit()
    sys.stdout=sys.__stdout__ 
    print("conversion successful")