import random
import json

from APIsolver import getAPIAnswer

def getAnswer(object):
    answer = ""
    with open("dictionary.txt","r") as file:
        dictionary = json.loads(file.read())
        if dictionary.__contains__(object["title"]):
            if dictionary[object["title"]] == object["answerA"]:
                answer = 'A'
            elif dictionary[object["title"]] == object["answerB"]:
                answer = 'B'
            elif dictionary[object["title"]] == object["answerC"]:
                answer = 'C'
            elif dictionary[object["title"]] == object["answerD"]:
                answer = 'D'  
    if answer == "":
        answer = getAPIAnswer(object)
    if answer == "":
        answer = ''.join(random.choice('ABCD'))
    return answer