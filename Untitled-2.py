from flask import Flask, render_template, request
import requests
from lxml import html
from bs4 import BeautifulSoup
import nltk
import pandas as pd
import io
import re
from nltk.corpus import stopwords
nltk.download('stopwords')

app = Flask(__name__)
word_list = {}
w = {}

@app.route('/')
def index ():
	
	df = pd.read_csv('Book1.csv')
	for i in range(0,len(df)):  
		web =  df['url'][i]
		resp = requests.get(web)
		soup = BeautifulSoup(resp.content,'html.parser')
		
		content = soup.find("body").get_text()
		text =re.findall(r"[\w']+", content.lower())
		w[i] = df['url'][i]
		addWord(text,i)

		


	# count =0

	# for i in list_text:
	# 	if i in word_list.keys():
	# 		count +=1  

	# s=[]
	# index=[]  
		
	# if len(list_text) > 1 and count == len(list_text):   
	# 	for i in range(len(word_list[list_text[0]])):        
	# 		a=[]       
	# 		for j in range(1,len(list_text)):
	# 			for k in range(len(word_list[list_text[j]])):
	# 				if word_list[list_text[0]][i][0] == word_list[list_text[j]][k][0]:
	# 					a.append(k)
	# 	s.append(a)         

		
	# 	for i in range(len(word_list[list_text[0]])):
	# 		num = 0
	# 		for j in range(len(s)):
	# 			if len(s[j]) == len(list_text)-1:
	# 				for x in range(len(word_list[list_text[0]][i][1])):
	# 					for k in range(1,len(list_text)):
	# 						n = word_list[list_text[0]][i][1][x] + k
	# 						if n in word_list[list_text[k]][s[j][k-1]][1]:
	# 							num +=1
			
	# 		if  num == len(list_text) -1:
	# 			index.append(word_list[list_text[0]][i][0])
	# 	if  len(index)> 0:  
	# 		for i in index:
	# 			print(i+1," ",df['url'][i])
	# 	else:
	# 		print("NOT FOUND")
	
	

      
	return render_template("tem.html")
	
@app.route('/result', methods = ['POST','GET'])	
def result	():
	
	if request.method == "POST":
		result = request.args
		word = request.form.get("Search").lower()
		
		l =[]
		for i in range(len(word_list[word])):
			l.append(w[word_list[word][i][0]])

		return render_template("result.html",result = l)


def addWord(word,count):
	stop_words = set(stopwords.words('english'))
	wordset =set(word)
	for i in wordset:
		if i not in stop_words :
			index =[ j for j,x in enumerate(word) if x==i]    
			if not i in word_list:
				word_list.update({i :[[count,index]]})
			else :
				word_list[i].append([count,index])
	
if __name__ == "__main__":
	app.run(debug =True)
	