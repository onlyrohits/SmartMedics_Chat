from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv

#####################################################################################
'''
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

'''

################################################################################################
'''
def symptom_specialist(words,dict_list):
	sym=[]
	special=[]
	word_length=len(words)
	for i in range (0,word_length):
		for j in dict_list:
			if i+4 < word_length:
				if words[i] in j['symptoms']:
					if words[i+1] in j['symptoms']:
						if words[i+2] in j['symptoms']:
							if words[i+3] in j['symptoms']:
								if words[i+4] in j['symptoms']:
									sym.append(words[i] + ' ' + words[i+1]+ ' ' + words[i+2] + ' ' + words[i+3]+ ' ' +words[i+4])
									special.append(j['specialist'])
								else:
									sym.append(words[i]+ " " + words[i+1]+ " " + words[i+2]+ " " + words[i+3])
									special.append(j['specialist'])
							else:
								sym.append(words[i]+ " " +words[i+1]+ " " +words[i+2])
								special.append(j['specialist'])
						else:
							sym.append(words[i]+ " " +words[i+1])
							special.append(j['specialist'])
					else:
						if words[i]==j['symptoms']:
							sym.append(words[i])
							special.append(j['specialist'])
			elif i+3 < word_length:
				if words[i] in j['symptoms']:
					if words[i+1] in j['symptoms']:
						if words[i+2] in j['symptoms']:
							if words[i+3] in j['symptoms']:
								sym.append(words[i]+ " " +words[i+1]+ " " +words[i+2]+ " " +words[i+3])
								special.append(j['specialist'])
							else:
								sym.append(words[i]+ " " +words[i+1]+ " " +words[i+2])
								special.append(j['specialist'])
						else:
							sym.append(words[i]+ " " +words[i+1])
							special.append(j['specialist'])
					else:						
						if words[i]==j['symptoms']:
							sym.append(words[i])
							special.append(j['specialist'])
			elif i+2 < word_length:
				if words[i] in j['symptoms']:
					if words[i+1] in j['symptoms']:
						if words[i+2] in j['symptoms']:
							sym.append(words[i]+ " " +words[i+1]+ " " +words[i+2])
							special.append(j['specialist'])
						else:
							sym.append(words[i]+ " " +words[i+1])
							special.append(j['specialist'])
					else:
						if words[i]==j['symptoms']:
							sym.append(words[i])
							special.append(j['specialist'])
			elif i+1 < word_length:
				if words[i] in j['symptoms']:
					if words[i+1] in j['symptoms']:
						sym.append(words[i]+ " " +words[i+1])
						special.append(j['specialist'])
					else:
						if words[i]==j['symptoms']:
							sym.append(words[i])
							special.append(j['specialist'])
			else:
				if words[i] in j['symptoms']:
					sym.append(words[i])
					special.append(j['specialist'])

	return (sym,special)
	'''

#############################################################################################

def symptom_specialist(words,dict_list):
	sym=[]
	special=[]
	string=" ".join(words)
	for i in dict_list:
		if i['symptoms'] in string:
			sym.append(i['symptoms'])
			special.append(i['specialist'])
	return (sym,special)

###############################################################################################

# To take a string as input and tokenise, lemmatize and conversion to lower case
sentence=input('Enter a string:')
sentence=sentence.lower()
lemma=WordNetLemmatizer()
temp=word_tokenize(sentence)
temp_words=[]
for m in temp:
	temp_words.append(lemma.lemmatize(m))

words=temp_words

##################################################################################################

# To read the CSV file as a list of dictionaries
reader=csv.DictReader(open('symptoms.csv','r'),fieldnames=('specialist','symptoms'))
dict_list=[]
for line in reader:
	dict_list.append(line)

####################################################################

# To check if the symptoms match those in the list of dictionaries and store it in another list sym[] and store corresponding specialists in special=[]
symptm,special=symptom_specialist(words,dict_list)
print(symptm,special)

'''
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

'''