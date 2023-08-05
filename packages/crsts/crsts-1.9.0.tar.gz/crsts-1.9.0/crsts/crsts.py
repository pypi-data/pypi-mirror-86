import os
import time
import hashlib
import shutil
import pickle
import base64
from multiprocessing import Process, JoinableQueue, Manager
import subprocess
from collections import Counter
import configparser
config = configparser.ConfigParser()
import csv
import random
import json
import glob

def write2path(lines,path='',encoding='utf-8',method='lines',append='w',wrap=False):
    if not path: path=getTime()+'.txt'
    with open(path,append,encoding=encoding) as fw:
        if method=='lines':
            lines = [str(f) for f in lines]
            if wrap: lines = [f+'\n' for f in lines]
            fw.writelines(lines)
        else:
            fw.write(lines)

def append2path(line,path,encoding='utf-8',method='line',append='a'):
    with open(path,append,encoding=encoding) as fw:
        if method=='line':
            fw.write(line+'\n')
        else:
            fw.writelines(line)

def read_path(path,method='lines',encoding='utf-8',errors='strict',strip=False):
    with open(path,'r',encoding=encoding,errors=errors) as fr:
        if method == "lines":
            all_lines = fr.readlines()
            if strip:
                all_lines = [l.strip() for l in all_lines]
        else:
            all_lines = fr.read()
        return all_lines

def print_list(array,index=False):
    if index:
        for i,val in enumerate(array):
            print(i,val)
    else:
        for val in array:
            print(val)
    print(f"length:{len(array)}")

def get_top_n_files(folder_path,n):
    if not os.path.exists(folder_path):
        return []
    if folder_path[-1] != '/':
        folder_path=folder_path+'/'
    top_n_files = [folder_path+f for f in os.listdir(folder_path)[:n]]
    return top_n_files

def copy_top_n_file(folder_path,n,dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    top_n_files = get_top_n_files(folder_path,n)
    for f in top_n_files:
        copyfile(f,dst_folder)

def save2pkl(obj,path,protocol=-1):
    with open(path,'wb') as fw:
        pickle.dump(obj,fw,protocol=protocol)

def read_pkl(path):
    with open(path, 'rb') as fr:
        obj = pickle.load(fr)
        return obj

def getTime(timestamp='',format='y'):
    if format=='y':
        format_str="%y-%m-%d %H:%M:%S"
    else:
        format_str="%Y-%m-%d %H:%M:%S"
    if timestamp:
        return time.strftime(format_str, time.localtime(timestamp))
    else:
        return time.strftime(format_str, time.localtime())

def getTimestamp():
    return time.time()

def getTimeSpan(begin_time, end_time, format='minute'):
    begin_time = time.strptime(begin_time, "%y-%m-%d %H:%M:%S")
    end_time = time.strptime(end_time, "%y-%m-%d %H:%M:%S")

    begin_timeStamp = int(time.mktime(begin_time))
    end_timeStamp = int(time.mktime(end_time))
    span_seconds = abs(end_timeStamp - begin_timeStamp)

    if format == 'second':
        return int(round(span_seconds, 2))
    elif format == 'minute':
        return int(round(span_seconds / 60, 2))
    elif format == 'hour':
        return int(round(span_seconds / 3600, 2))
    elif format == 'day':
        return int(round(span_seconds / 86400, 2))
    else:
        return int(round(span_seconds, 2))

def get_file_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5

def get_str_md5(parmStr):
    if isinstance(parmStr, str):
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()

def getfilesize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / (1000 * 1000)
    return round(fsize, 2)

def listDir(rootDir,only_file=False,only_folder=False,recursive=False):
    list_filepath = []
    if recursive:
        all_file=glob.glob(os.path.join(rootDir, '**'), recursive=True)
        for pathname in all_file:
            filename = os.path.basename(pathname)
            if filename == '.DS_Store':
                continue
            if only_file:
                if os.path.isfile(pathname):
                    list_filepath.append(pathname)
                continue
            if only_folder:
                if os.path.isdir(pathname):
                    list_filepath.append(pathname)
                continue
            list_filepath.append(pathname)
    else:
        for filename in os.listdir(rootDir):
            pathname = os.path.join(rootDir, filename)
            if filename == '.DS_Store':
                continue
            if only_file:
                if os.path.isfile(pathname):
                    list_filepath.append(pathname)
                continue
            if only_folder:
                if os.path.isdir(pathname):
                    list_filepath.append(pathname)
                continue
            list_filepath.append(pathname)
    return list_filepath

def makedir(dir_path,delete_exists=False):
    if os.path.exists(dir_path):
        if delete_exists:
            rmfolder(dir_path)
            os.makedirs(dir_path)
        else:
            print("--------创建文件夹失败:" + dir_path + ",路径已存在--------")
    else:
        os.makedirs(dir_path)

def touchfile(path):
    if not os.path.exists(path):
        f = open(path,'w')
        f.close()

def counter(lst,sort=False,reverse=False):
    if sort:
        sorted_lst=sorted(Counter(lst).items(),key=lambda f:f[1],reverse=reverse)
        return dict(sorted_lst)
    else:
        return dict(Counter(lst))

def copyfile(origin_path, target_path):
    if os.path.isfile(origin_path):
        shutil.copy(origin_path, target_path)
    else:
        print("--------复制文件失败:" + origin_path + ",路径不存在--------")

def movefile(origin_path, target_path):
    if os.path.isfile(origin_path):
        shutil.move(origin_path, target_path)
    else:
        print("--------移动文件失败:" + origin_path + ",路径不存在--------")

def copyfolder(origin_folder, target_folder, *args):
    # 目标文件夹名为 target_path，不能已经存在；方法会自动创建目标文件夹。
    if os.path.isdir(origin_folder):
        shutil.copytree(origin_folder, target_folder, ignore=shutil.ignore_patterns(*args))
    else:
        print("--------复制文件夹失败:" + origin_folder + ",路径不存在--------")

def rmfile(del_file):
    if os.path.isfile(del_file):
        os.remove(del_file)
    else:
        print("--------删除文件失败:" + del_file + ",路径不存在--------")

def rmfolder(del_folder):
    if os.path.isdir(del_folder):
        shutil.rmtree(del_folder)
    else:
        print("--------删除文件夹失败:" + del_folder + ",路径不存在--------")

def base64decode(strings,encoding='utf-8'):
    try:
        base64_decrypt = base64.b64decode(strings.encode('utf-8'))
        return str(base64_decrypt, encoding)
    except:
        return ''

def base64encode(strings,encoding='utf-8'):
    try:
        base64_encrypt = base64.b64encode(strings.encode('utf-8'))
        return str(base64_encrypt, encoding)
    except:
        return ''

def run_cmd(cmd,with_output=False):
    if with_output:
        return subprocess.getstatusoutput(cmd)
    else:
        return subprocess.call(cmd, shell=True)

def func_time(func):
    begin_time= time.time()
    func()
    end_time= time.time()
    print(f'{func.__name__} 耗时:{int(end_time-begin_time)}')

def run_multi_task(all_items, user_func, cpu_num=os.cpu_count()):
    print(f'检测到全部:{len(all_items)}个')
    print(f'启动{cpu_num}个进程,开始运行')

    if len(all_items)>32000:
        print('数组个数大于32000，无法运行')
        return []
    else:
        begin_time = time.time()
        q = JoinableQueue()
        for item in all_items:
            q.put(item)

        def func_task(q, res_list):
            while True:
                item = q.get()
                res_list.append(user_func(item))
                q.task_done()

        res_list = Manager().list()
        for i in range(cpu_num):
            p = Process(target=func_task, args=(q, res_list))
            p.daemon = True
            p.start()
        q.join()
        print(f'全部已完成，用时:{float(time.time() - begin_time)}')
        return list(res_list)

def run_multi_task_in_order(all_items, user_func, cpu_num=os.cpu_count()):
    print(f'检测到全部:{len(all_items)}个')
    print(f'启动{cpu_num}个进程,开始运行')

    if len(all_items)>32000:
        print('数组个数大于32000，无法运行')
        return {}
    else:
        begin_time = time.time()
        q = JoinableQueue()
        for index,data in enumerate(all_items):
            q.put((index,data))

        def func_task(q, res_dict):
            while True:
                item = q.get()
                res_dict[item[0]] = user_func(item[1])
                q.task_done()

        res_dict = Manager().dict()
        for i in range(cpu_num):
            p = Process(target=func_task, args=(q, res_dict))
            p.daemon = True
            p.start()
        q.join()
        print(f'全部已完成，用时:{float(time.time() - begin_time)}')
        return dict(res_dict)

def read_config(config_path,config_name,section='default',type='str'):
    config = configparser.ConfigParser()
    config.read(config_path)
    if section in config.sections():
        if config_name in config.options(section):
            if type=='str':
                return config.get(section, config_name)
            elif type=='float':
                return config.getfloat(section, config_name)
            elif type=='int':
                return config.getint(section, config_name)
            elif type=='bool':
                return config.getboolean(section, config_name)
    return ''

def write_config(config_path,config_name,config_value,section='default'):
    config = configparser.ConfigParser()
    config.read(config_path)
    if not config.has_section(section): config.add_section(section)
    config.set(section, config_name, config_value)

    with open(config_path, 'w') as configfile:
        config.write(configfile)

def read_csv(csv_path,method="list",encoding='utf-8',header=False):
    '''
    :param method: list or dict
    :param return: [[1, 'chen', 'male']]  or [[('age', '1'), ('name', 'chen'), ('sex', 'male')]]
    '''
    csv_cnts=[]
    headers=[]
    with open(csv_path, encoding=encoding) as f:
        if method=="list":
            reader = csv.reader(f)
            headers.extend(next(reader))
            for row in reader:
                csv_cnts.append(row)
        else:
            reader = csv.DictReader(f)
            headers.extend(list(next(reader).keys()))
            for row in reader:
                csv_cnts.append(row)
    if header:
        return headers,csv_cnts
    else:
        return csv_cnts

def write_csv(csv_path,header=[],rows=[],method="list",encoding='utf-8',append='w'):
    '''
    :param header: ['name', 'age', 'sex']
    :param rows: [{'age': 1, 'name': 'chen', 'sex': 'male'}] or [[1, 'chen', 'male']]
    :param method: list or dict
    '''
    with open(csv_path, append, encoding=encoding, newline='') as f:
        if method=="list":
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        else:
            writer = csv.DictWriter(f, header)
            writer.writeheader()
            writer.writerows(rows)

def rand_int(min,max):
    return random.randint(min, max)

def rand_choice(lst):
    result=random.choice(lst)
    return result

def rand_choices(lst,k=1):
    result=random.choices(lst,k=k)
    return result

def rand_sample(lst, k=1):
    result=random.sample(lst, k)
    return result

def rand_shuffle(lst):
    random.shuffle(lst)
    return lst

def json_load(fp):
    return json.load(fp)

def json_loads(json_str):
    return json.loads(json_str)

def json_dump(json_data, fp):
    return json.dump(json_data, fp)

def json_dumps(json_data):
    return json.dumps(json_data)

def sleep(secs):
    time.sleep(secs)

def change_venv(old_project_path,new_project_path):
    '''
        解决venv修改位置后失效问题
    '''
    activate_path1=os.path.join(new_project_path,"venv/bin/activate")
    activate_path2=os.path.join(new_project_path,"venv/bin/activate.csh")
    activate_path3=os.path.join(new_project_path,"venv/bin/activate.fish")

    pip_path1=os.path.join(new_project_path,"venv/bin/pip")
    pip_path2=os.path.join(new_project_path,"venv/bin/pip3")
    pip_path3=os.path.join(new_project_path,"venv/bin/pip3.6")

    for f in [activate_path1,activate_path2,activate_path3,pip_path1,pip_path2,pip_path3]:
        cnt=read_path(f,method="line")
        cnt=cnt.replace(old_project_path,new_project_path)
        write2path(cnt,f,method="line")


