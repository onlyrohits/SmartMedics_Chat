from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv


# Function to remove stopwords and clean the string
def parsing(word):
	words=[]
	stop_words = set(stopwords.words('english'))
	stop_words.add('to')
	for element in word:
		if not (element == ',' or element =='.' or element ==':') :
			if element not in stop_words:
				if ":" in element:
					split_list=element.split(":")
					words.extend(split_list)
				else:
					words.append(element)
	return words


# To take a string as input and tokenise, lemmatize and conversion to lower case
sentence=input('Enter a string:')
sentence=sentence.lower()
lemma=WordNetLemmatizer()
temp=word_tokenize(sentence)
temp_words=[]
for m in temp:
	temp_words.append(lemma.lemmatize(m))
words=parsing(temp_words)
print (words)


# To read the CSV file as a list of dictionaries
reader=csv.DictReader(open('symptoms.csv','r'),fieldnames=('specialist','symptoms'))
dict_list=[]
for line in reader:
	dict_list.append(line)


# To check if the symptoms match those in the list of dictionaries and store it in another list sym[] and store corresponding specialists in special=[]
sym=[]
special=[]
for i in words:
	for j in dict_list:
		if i==j['symptoms']:
			sym.append(i)
			special.append(j['specialist'])
print(sym)
print(special)


# To convert the results into percentages
for i in special:
	i=i.lower() #only to convert matching strings to same format
print(special)
count={} #will work as a flag to count how many times a specialist has been recommended
for i in special:
	if i in count.keys():
		count[i]=count[i]+1
	else:
		count[i]=1
print(count)