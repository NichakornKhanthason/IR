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


countin = 0
word =[]
j = open('list_invert.json')
word = json.load(j)
j.close()
			

counthash = 0
wordhash ={}
j = open('dicthash.json')
wordhash = json.load(j)
j.close()


counttree =0
wordtree = {}
arrtree =[]
textinput = ""
j = open('dictree.json')
wordtree = json.load(j)
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
    
    global countin 
    global countpo
    global counthash
    global counttree
    countin = 0
    countpo = 0
    counthash = 0
    counttree = 0
    ###--inverted---###
    dictin ={}      
    for i in list_text:
      urlin =[]
      text = checkword(i)
      if text != "No Word":
        for j in text[1]:
          urlin.append(df['url'][j])  
        dictin[text[0]]  = urlin
      else:
        dictin[i]  = ["NOT FOUND"]



    ###---position---###      
    count =0
    dictpo={}
    url=[]
        
    for i in list_text:
      if i in word_list.keys():
        count +=1

    if len(list_text) > 1 and count == len(list_text):
      listindex = checkposition(list_text,count)
      if listindex != "NOT FOUND":
        for i in listindex:
          url.append(df['url'][i])
        dictpo[word] = url
      else:
        dictpo[word]=["NOT FOUND"]

    elif len(list_text) ==1 and list_text[0]  in word_list.keys():
      for i in range(0,len(word_list[list_text[0]])):
          url.append(df['url'][word_list[list_text[0]][i][0]])
      dictpo[word] = url   
    else:
      dictpo[word]=["NOT FOUND"]

    ####--hash--##
    urlhash =[]
    h= HashMap()
    dicthash ={}
    for j in wordhash:
      h.add(j,wordhash[j])
    if count == len(list_text):
      for i in list_text:
        if i in wordhash:
          urlhash.append(list(h.get(i)))
      urlhashin = intersechash(urlhash)
      dicthash[word] = urlhashin
    else:
      dicthash[word] = ["NOT FOUND"]

   
    

    ##--tree--###
    global textinput
    dicttree={}
    lendic = len(wordtree)
    mid = lendic//2

    for i,w in enumerate(wordtree):
      counttree+=1
      if i == mid:
        datanode = chdic(wordtree,w)       
    r = Node(datanode)
    for i,w in wordtree.items():
      counttree+=1
      array = chdic(wordtree,i)
      insert(r,Node(array))
    
    if count == len(list_text):
      for i in list_text:
        textinput = i
        inorder(r)
      link = intersec(arrtree)
      dicttree[word] = list(link)
    else:
      dicttree[word] = ["NOT FOUND"]


    
   
    
    return render_template("result.html",resultin = dictin ,resultin1=countin ,resultpo=dictpo,resultpo1=countpo,resulthash=dicthash,resulthash1=counthash,resulttree=dicttree,resulttree1=counttree)



def splitword(word):
  tokens = re.findall("[A-Za-z]+",word.lower())
  stop_words = set(stopwords.words('english'))
  listtext = []
  for i in tokens:
    if i not in stop_words:
      listtext.append(i)  
  return listtext

def intersec(a):
  s1={}
  for i in  range (0,len(a)):
    if i == 0:
      s1 = set(a[i][1])
    if i < len(a)-1:
      s1 = s1.intersection(set(a[i+1][1]))
    if len(s1) == 0:
      return {"NOT FOUND"}
  return s1


def intersechash(a):
  s1={}
  for i in  range (0,len(a)):
    if i == 0:
      s1 = set(a[i])
    if i < len(a)-1:
      s1 = s1.intersection(set(a[i+1]))
    if len(s1) == 0:
      return {"NOT FOUND"}
  return s1


####--inverted--###
def checkword(text):
    for i in range(0,len(word)):
        if  text == word[i][0]:
            return word[i]
        global countin 
        countin+=1
    return "No Word"


####--position---####
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

 #### ---hash --####
class HashMap:
  def __init__(self):
    self.size = 15551
    self.map = [None] * self.size
		
  def _get_hash(self, key):
    global counthash
    hash = 0
    for char in str(key):
      counthash+=1
      hash += ord(char)
    return hash % self.size
		
  def add(self, key, value):
    global counthash
    key_hash = self._get_hash(key)
    key_value = [key, value]
		
    if self.map[key_hash] is None:
      self.map[key_hash] = list([key_value])
      counthash+=1
      return True
    else:
      for pair in self.map[key_hash]:
        counthash=+1
        if pair[0] == key:
          pair[1] = value
          return True
        self.map[key_hash].append(key_value)
      return True
			
  def get(self, key):
    global counthash
    key_hash = self._get_hash(key)
    if self.map[key_hash] is not None:
      for pair in self.map[key_hash]:
        counthash+=1
        if pair[0] == key:
          return pair[1]
        return None   


###--  binarysearchtreee --- ####
class Node: 
    def __init__(self,key): 
        self.left = None
        self.right = None
        self.val = key 
  
# A utility function to insert a new node with the given key 
def insert(root,node): 
      global counttree
      if root is None:
          counttree+=1
          root = node 
      else: 
          if root.val < node.val:
              counttree+=1 
              if root.right is None:
                  counttree+=1 
                  root.right = node 
              else: 
                  counttree+=1
                  insert(root.right, node) 
          else: 
              if root.left is None:
                  counttree+=1 
                  root.left = node 
              else: 
                  insert(root.left, node)
                  counttree+=1

  
# A utility function to do inorder tree traversal 
def inorder(root):
      global arrtree
      global counttree
      if root:
          global textinput 
          counttree+=1
          inorder(root.left)
          if root.val[0]== textinput:
            counttree+=1
            arrtree.append(root.val)
          inorder(root.right)

def chdic(data,word):
  arr = []
  for i,v in data.items():
    counttree+=1
    if i == word:
      arr.append(i),arr.append(set(v))
  return arr    


if __name__ == "__main__":
	app.run(debug =True)
	