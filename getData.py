import requests
import random
import string
import time
import json

from solver import getAnswer

WEEK = '5' #第几周
XAUTHTOKEN = ["<localStorage.sessionId>1","<localStorage.sessionId>2"]#浏览器控制台或者抓包看
TIME = 110 #预期考试时间
HOST = "http://skl.hdu.edu.cn"

flag = 0 #report the error ,1 for error
ttt = 0 #遍历Token的键值

body = {}

def X_Auth_Token():
    return XAUTHTOKEN[ttt]

def Skl_Ticket():
    length_of_string = 21
    dict_or_string = string.ascii_letters + string.digits + '-'
    return ''.join(random.choice(dict_or_string) for _ in range(length_of_string))

def options_query():
    return '?' + 'type=' + '0' + '&week=' + WEEK + '&startTime=' + str(time.time()).replace('.', '')[:-4]

def visit_exam_api():
    suffix = "/api/paper/new"
    url = HOST + suffix + options_query()
    requests.options(url)

    headers ={"X-Auth-Token": X_Auth_Token(),
              "Skl-Ticket": Skl_Ticket()}
    content = requests.get(url, headers = headers).content.decode('utf8')
    questions_obj = json.loads(content)
    if questions_obj.__contains__("code"):
        print(f"Token {str(ttt)} jumped" )
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
              "Content-Type": "application/json"}
    time.sleep(TIME)
    requests.post(url=url, headers=headers, data=json.dumps(body))

def save_volca():
    global dictionary
    suffix = "/api/paper/detail"
    url = HOST + suffix + '?paperId=' + body["paperId"]
    requests.options(url)
    headers ={"X-Auth-Token": X_Auth_Token(),
              "Skl-Ticket": Skl_Ticket(),
              "Content-Type": "application/json"}
    obj = json.loads(requests.get(url=url, headers=headers).text)
    for que in obj["list"]:
        if not dictionary.__contains__(que["title"]):
            dictionary[que["title"]] = que["answer" + que["answer"]]

if __name__ == "__main__":
    times = 0
    while True:
        with open("dictionary.txt","r") as file:
            dictionary = json.loads(file.read())
            try:
                flag = 0
                visit_exam_api()
                save_volca()
            except Exception as e:
                print(e)
        if flag == 0:
            with open("dictionary.txt","w") as file:
                file.write(json.dumps(dictionary))
        
        ttt = (ttt + 1) % len(XAUTHTOKEN)
        if ttt == 0:
            print(str(times))
            times = times + 1
        exit()


