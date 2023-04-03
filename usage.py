import requests
import random
import string
import time
import json

from solver import getAnswer

TYPE = '1' #0自测，1考试
WEEK = '5' #第几周
TIME = 300 #考试时间(sec)

flag = 0 #report the error , 1 for error
ttt = 0

XAUTHTOKEN = ["ea4454bc-767b-4a0c-a640-49ecee6418c7"]#浏览器控制台或者抓包看

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
    content = requests.get(url, headers = headers).content.decode('utf8')
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
    time.sleep(TIME)
    requests.post(url=url, headers=headers, data=json.dumps(body))


if __name__ == "__main__":
    times = 0
    while True:
        with open("dictionary.txt","r") as file:
            dictionary = json.loads(file.read())
            try:
                flag = 0
                visit_exam_api()
            except Exception as e:
                print(e)
        if flag == 0:
            with open("dictionary.txt","w") as file:
                file.write(json.dumps(dictionary))
        
        ttt = (ttt + 1) % len(XAUTHTOKEN)
        if ttt == 0:
            # os.system(f"cp dictionary.txt dictionary{str(times)}.txt")
            times = times + 1
        exit()


