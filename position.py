from flask import Flask, render_template, request
import requests
from lxml import html
from bs4 import BeautifulSoup
import nltk
import pandas as pd
import io
import re
import json
from nltk.corpus import stopwords
nltk.download('stopwords')

app = Flask(__name__)
word_list = {}
w = {}
df = pd.read_csv('Book1.csv')
countpo=0
j = open('dictpo.json')
word_list = json.load(j)
j.close()
			
	

@app.route('/')
def index ():

	  
    return render_template("tem.html")
	
@app.route('/result', methods = ['POST','GET'])	
def result	():	
    if request.method == "POST":
        result = request.args
        word = request.form["Search"]
        list_text = splitword(word)
        print(list_text)
		
		      
        count =0
        dictword={}
        url=[]
        
        for i in list_text:
            if i in word_list.keys():
                count +=1

        if len(list_text) > 1 and count == len(list_text):
            listindex = checkposition(list_text,count)
            if listindex != "NOT FOUND":
                for i in listindex:
                    url.append(df['url'][i])
                dictword[word] = url
            else:
                dictword[word]=["NOT FOUND"]

        elif len(list_text) ==1 and list_text[0]  in word_list.keys():
            for i in range(0,len(word_list[list_text[0]])):
                url.append(df['url'][word_list[list_text[0]][i][0]])
            dictword[word] = url   
        else:
            dictword[word]=["NOT FOUND"]

        return render_template("result.html",result = dictword ,result1=countpo )



def splitword(word):
    tokens = re.findall(r"[\w']+",word.lower())
    return tokens


def checkposition(list_text,count):    
    s=[]
    index=[]
    global countpo   
        
    for i in range(len(word_list[list_text[0]])):
        countpo +=1        
        a=[]       
        for j in range(1,len(list_text)):
            countpo +=1
            for k in range(len(word_list[list_text[j]])):
                countpo +=1
                if word_list[list_text[0]][i][0] == word_list[list_text[j]][k][0]:
                    a.append(k)
            s.append(a)         

        
    for i in range(len(word_list[list_text[0]])):
        num = 0
        countpo +=1
        for j in range(len(s)):
            countpo +=1
            if len(s[j]) == len(list_text)-1:
                countpo +=1
                for x in range(len(word_list[list_text[0]][i][1])):
                    countpo +=1
                    for k in range(1,len(list_text)):
                        countpo +=1
                        n = word_list[list_text[0]][i][1][x] + k
                        if n in word_list[list_text[k]][s[j][k-1]][1]:
                            num +=1
        
        if  num == len(list_text) -1:
            countpo +=1
            index.append(word_list[list_text[0]][i][0])
    if  len(index)> 0:  
        return index
    else:
        return "NOT FOUND"
    

if __name__ == "__main__":
	app.run(debug =True)
	