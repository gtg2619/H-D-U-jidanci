# -- coding: utf-8 --

import requests
import random
import string
import time
import json
import sys

from solver import getAnswer

TYPE = '0' #0自测，1考试
WEEK = '5' #第几周
TIME = 300  #考试时间(sec)

flag = 0 #report the error , 1 for error
ttt = 0
XAUTHTOKEN = ['792a7e91-31e7-4cde-a366-1c95d6b05b50']#浏览器控制台或者抓包看

HOST = "http://skl.hdu.edu.cn"

body = {}

def X_Auth_Token():
    return XAUTHTOKEN[ttt]

def Skl_Ticket():
    length_of_string = 21
    dict_or_string = string.ascii_letters + string.digits + '-'
    return ''.join(random.choice(dict_or_string) for _ in range(length_of_string))

def options_query():
    return '?' + 'type=' + TYPE + '&week=' + WEEK + '&startTime=' + str(time.time()).replace('.', '')[:13]

def visit_exam_api():
    suffix = "/api/paper/new"
    url = HOST + suffix + options_query()
    requests.options(url)

    headers ={"X-Auth-Token": X_Auth_Token(),
              "Skl-Ticket": Skl_Ticket(),
              "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/10.3 SearchCraft/2.6.2 (Baidu; P1 7.0)"
              }
    content = requests.get(url, headers = headers).text
    if content == "":
        print('Token失效')
        exit
    questions_obj = json.loads(content)
    if questions_obj.__contains__("code"):
        print(f"Token {str(ttt)} jumped" )
        print(questions_obj["msg"])
        flag = 1
        return "failed"
    else:
        print(f"Token {str(ttt)} worked")
    visit_save_api(get_save_body(questions_obj))

def get_save_body(questions_obj):
    body["paperId"] = questions_obj["paperId"]
    body["type"] = questions_obj["type"]

    body["list"] = []
    for question in questions_obj["list"]:
        paperDetailId = question["paperDetailId"]
        answer = getAnswer(question)
        body["list"].append({"input":answer,"paperDetailId":paperDetailId})
    return body

def visit_save_api(body):
    suffix = "/api/paper/save"
    url = HOST + suffix
    requests.options(url)

    headers ={"X-Auth-Token": X_Auth_Token(),
              "Skl-Ticket": Skl_Ticket(),
              "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/10.3 SearchCraft/2.6.2 (Baidu; P1 7.0)",
              "Content-Type": "application/json"}
    while True:
        time.sleep(1)
        if int(time.time()) - startTime >= TIME:
            break
    requests.post(url=url, headers=headers, data=json.dumps(body))

def getTimeStamp():
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime)
    return now

if __name__ == "__main__":
    print("start at ", end="")
    startTime = getTimeStamp()
    try:
        requests.get(url=f"https://cdn.jsdelivr.net/gh/lyc8503/baicizhan-word-meaning-API/data/words/word.json",verify=False).content.decode("unicode_escape")
    except Exception as e:
        print('API风控或网络错误，进程结束')
        sys.exit()
    with open("dictionary.txt","r") as file:
        dictionary = json.loads(file.read())
        try:
            flag = 0
            visit_exam_api()
        except Exception as e:
            print(e)
    print("end at ", end="")
    endTime = getTimeStamp()
    print(f"totally spend {endTime-startTime} seconds")



