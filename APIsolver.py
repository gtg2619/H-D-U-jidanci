import random
import json
import requests
import time

import warnings

warnings.filterwarnings("ignore")

def getAPIAnswer(object):
    answer = ""
    object["title"] = object["title"].strip(" . ")
    for char in "ABCD":
        object["answer"+char] = object["answer"+char].strip(" . ")
    if  '\u4e00' <= object["title"] <= '\u9fa5':
        for char in "ABCD":
            try:
                text = requests.get(url=f"https://cdn.jsdelivr.net/gh/lyc8503/baicizhan-word-meaning-API/data/words/{object['answer'+char]}.json",verify=False).content.decode("unicode_escape")
            except Exception as e:
                time.sleep(1)
                text = requests.get(url=f"https://cdn.jsdelivr.net/gh/lyc8503/baicizhan-word-meaning-API/data/words/{object['answer'+char]}.json",verify=False).content.decode("unicode_escape")
            if object["title"] in text:
                answer = char
                break

    else:
        try:
            text = requests.get(url=f"https://cdn.jsdelivr.net/gh/lyc8503/baicizhan-word-meaning-API/data/words/{object['title']}.json",verify=False).content.decode("unicode_escape")
        except:
            text = requests.get(url=f"https://cdn.jsdelivr.net/gh/lyc8503/baicizhan-word-meaning-API/data/words/{object['title']}.json",verify=False).content.decode("unicode_escape")
        for char in "ABCD":
            if object['answer'+char] in text:
                answer = char
                break
    
    if answer == "":
        answer = ''.join(random.choice('ABCD'))
    return answer

# if __name__ == "__main__":
#     object ={
#         "title":"scarcely .",
#         "answerA":"害怕地 .",
#         "answerB":"神圣地 .",
#         "answerC":"仅仅 .",
#         "answerD":"恐惧的"
#     }
#     print(getAnswer(object))