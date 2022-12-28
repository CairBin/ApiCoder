import sys,os
import json

def read_file(filepath:str,enconding='utf-8'):
    content = ''
    try:
        with open(filepath,'r',encoding=enconding) as fp:
            content = fp.read()
        return content
    except:
        print('错误：文件读取发生异常 ' + filepath)
        sys.exit()


def read_json(filepath:str,enconding='utf-8'):
    json_data = ''
    try:
        with open(filepath,'r',encoding=enconding) as fp:
            json_data = json.load(fp)
        return json_data
    except:
        print('错误：Json文件读取发生异常 ' + filepath)
        sys.exit()


def check_dir(path:str)->bool:
    if os.path.isdir(path):
        return True
    return False

def make_dir(path:str):
    try:
        os.mkdir(path)
    except:
        print('错误：创建目录失败 ' + path)
        sys.exit()

def write_file(filepath:str,content,enconding='utf-8'):
    try:
        with open(filepath, 'w', encoding=enconding) as fp:
            fp.write(content)
    except:
        print('错误：文件写入异常 ' + filepath)
