from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv
#################################################################################

def parsing(words):
	word_list=[]
	stop_words = set(stopwords.words('english'))
	stop_words.add('to')
	for element in words:
		if not (element == ',' or element =='.' or element ==':') :
			if element not in stop_words:
				if ":" in element:
					split_list=element.split(":")
					word_list.extend(split_list)
				else:
					word_list.append(element)
	return word_list

##################################################################################

def age_extraction(words):
	number_index=[]
	size=len(words)
	age=0
	for i in range (0,size):
		try:
			age_temp=float(words[i])
			if words[i+1]=='year' and (words[i+2]!='and' or words[i+3]!='month'):
				age=age_temp
				break
			elif words[i+1]=='month':
				age=age_temp/12
				break
			elif words[i+1]=='year' and words[i+2]=='and' and words[i+4]=='month':
				try:
					month_temp=float(words[i+3])
					age = age + month_temp/12
					break
				except ValueError:
					month_temp=text2int(words[i+3])
					age = age + month_temp/12
					break
			elif words[i+1]=='year' and words[i+2]!='and' and words[i+3]=='month':
				try :
					month_temp=float(words[i+3])
					age = age + month_temp/12
					break
				except ValueError:
					month_temp=text2int(words[i+2])
					age= age + month_temp/12
					break
			else:
				continue
		except :
			try:
				age_temp=text2int(words[i])
				try:
					age_temp1=text2int(words[i+1])
					if words[i+2]=='year' and (words[i+3]!='and' or words[i+3]!='month'):
						age=age_temp + age_temp1
						break
					elif words[i+1]=='month':
						age=(age_temp+age_temp1)/12
						break
					elif words[i+2]=='year' and words[i+3]=='and' and words[i+5]=='month':
						try:
							month_temp=float(words[i+4])
							age = age_temp + age_temp1 + month_temp/12
							break
						except ValueError:
							month_temp=text2int(words[i+4])
							age = age_temp + age_temp1 + month_temp/12
							break
					elif words[i+2]=='year' and words[i+3]!='and' and words[i+5]=='month':
						try :
							month_temp=float(words[i+3])
							age = age_temp1 + age_temp + month_temp/12
							break
						except ValueError:
							month_temp=text2int(words[i+3])
							age= age_temp + age_temp1 + month_temp/12
							break

				except:
					if words[i+1]=='year' and (words[i+2]!='and' or words[i+3]!='month'):
						age=age_temp
						break
					elif words[i+1]=='month':
						age=age_temp/12
						break
					elif words[i+1]=='year' and words[i+2]=='and' and words[i+4]=='month':
						try:
							month_temp=float(words[i+3])
							age = age + month_temp/12
							break
						except ValueError:
							month_temp=text2int(words[i+3])
							age = age + month_temp/12
							break
					elif words[i+1]=='year' and words[i+2]!='and' and words[i+3]=='month':
						try :
							month_temp=float(words[i+2])
							age = age + month_temp/12
							break
						except ValueError:
							month_temp=text2int(words[i+2])
							age= age + month_temp/12
							break
					else:
						continue
			except :
				continue
	return age

##############################################################################################

def text2int(textnum, numwords={}):
    if textnum=='half':
      return 0.5
    elif textnum=='quarter':
      return 0.25   
    elif not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current



###############################################################################################

description=input("Enter String: ")
lemma=WordNetLemmatizer()
temp=word_tokenize(description)
temp_words=[]
for m in temp:
	temp_words.append(lemma.lemmatize(m))
word_list=parsing(temp_words)
print(word_list)

##################################

male=[]
female=[]
filename='MaleFemale.csv'
dataset=pd.read_csv(filename)
array=dataset.values
for i in array:
	male.append(i[0])
	female.append(i[1])

#####################################################

gender=''
for sex in word_list:
	if sex in male:
		gender='Male'
		break
	elif sex in female:
		gender='Female'
		break

#######################################################

age=age_extraction(word_list)
print(age)

