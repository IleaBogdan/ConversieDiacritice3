import os
import sys
import chardet
import shutil
import json
from time import sleep

# exePath=os.getcwd()

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
        print(file)
    else:
        print("No file provided!")
        sleep(10)
        return
    
    # loading replacement chars
    # with open("map.json") as config:
    #    charMap=json.load(config)
    # print(charMap)
    charMap={
        "\u00ba": "s",
        "\u00fe": "t",
        "\u00aa": "S",
        "\u00de": "T" 
    }

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
    with open('C:/Work/Proiecte_serioase/ConversieDiacritice3/log.txt', 'w') as f:
        sys.stdout = f
        try:
            main()
        except Exception as e:
            print(e)
            sys.stdout=sys.__stdout__ 
            print("conversion failed, check log.txt to see the error")
            exit()
    sys.stdout=sys.__stdout__ 
    print("conversion successful")