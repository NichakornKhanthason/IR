from flask import Flask, render_template, request
import requests
from lxml import html
from bs4 import BeautifulSoup
import nltk
import pandas as pd
import io
import re
import json

app = Flask(__name__)
countin = 0
word =[]

df = pd.read_csv('Book1.csv')
j = open('list_inver.json')
word = json.load(j)
j.close()
			
@app.route('/')
def index ():
    global count
   
    # for i in range(0,len(df)):  
    #     web = df['url'][i]
    #     resp = requests.get(web)
    #     soup = BeautifulSoup(resp.content,'html.parser')
    
    #     content = soup.find("body").get_text()
    #     tokens =re.findall(r"[\w']+", content.lower())
    
    #     for j in set(tokens):
    #         word.append([j,[i],1])

    # word.sort()
    # i=0
    # while i < len(word):
    #     if i< len(word)-1:
    #         if word [i][0] == word [i+1][0]:
    #             word [i][2] +=1
    #             word[i][1].append(word[i+1][1][0])
    #             del word[i+1]
    #             count+=1
    #         else:
    #             i+=1
    #             count+=1
    #     else:
    #         i+=1
    return render_template("tem.html")

@app.route('/result', methods = ['POST','GET'])	
def result	():
    if request.method == "POST":
        result = request.args
        words = request.form["Search"]
        list_text = splitword(words)
        l =[]
        dictin ={}
        
        for i in list_text:
            urlin =[]
            text = checkword(i)
            if text != "No Word":
                for j in text[1]:
                    urlin.append(df['url'][j])  
                dictin[text[0]]  = urlin                         
        return render_template("result.html",result = dictin,result1 = countin)




def splitword(word):
    tokens = re.findall(r"[\w']+",word.lower())
    return tokens

def checkword(text):
    for i in range(0,len(word)):
        if  text == word[i][0]:
            return word[i]
        global countin 
        countin+=1
    return "No Word"

if __name__ == "__main__":
	app.run(debug =True)
	