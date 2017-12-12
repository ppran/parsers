#This code scans current.txt and system-current.txt and convert it to Eagle Eye format of file "fr_sys_apis.config"


import sys
import re


with open("current.txt") as f:
	text=f.readlines();

listOfAPI = set()
count=0
classfound=False
abstractclass=False
for record in text:
	if re.search("package",record):
		packagewords=re.split('\s+',record)
		if packagewords[1]!="field":
			packagename=packagewords[1]
			packagename=packagename.replace('.','/')

		#packagename=record
	if re.search("class",record):
		abstractclass=False
		nameClass=re.split('\s+',record)
		for i in nameClass:
			if classfound==True:
				className=i
				classfound=False
				break
			if i=="class":
				classfound=True
			if i=="abstract":
				abstractclass=True


		#print packagename + "->" + nameClass[-3]

	if re.search("method",record):
		methodClass=re.split('\s+',record)
		for item in methodClass:
			if re.search("\(",item):
				item=re.split("\(",item)[0]
				count=count+1
				if re.search("abstract",record) or abstractclass:
					pass
				else:
					listOfAPI.add("L" + packagename + "/" + className + ";"+ "->" + item)



with open("system-current.txt") as f:
	text=f.readlines();


classfound=False
for record in text:
	if re.search("package",record):
		packagewords=re.split('\s+',record)
		if packagewords[1]!="field":
			packagename=packagewords[1]
			packagename=packagename.replace('.','/')

		#packagename=record
	if re.search("class",record):
		abstractclass=False
		nameClass=re.split('\s+',record)
		for i in nameClass:
			if classfound==True:
				className=i
				classfound=False
				break
			if i=="class":
				classfound=True

			if i=="abstract":
				abstractclass=True


		#print packagename + "->" + nameClass[-3]

	if re.search("method",record):
		methodClass=re.split('\s+',record)
		for item in methodClass:
			if re.search("\(",item):
				item=re.split("\(",item)[0]
				count=count+1
				if re.search("abstract",record) or abstractclass:
					pass
				else:
					listOfAPI.add("L" + packagename + "/" + className + ";"+ "->" + item)



for api in listOfAPI:
	print api

# print len(listOfAPI) Total 24498



'''			
			if re.search("\(",item):
				if re.search("\)",item):
					print "L" + packagename + "/" + className + ";" + "->" + item
				else:
					#item = item.split("(")
					#print item
					item = item.split("(")[0]+'()'
					#item= item+')'
					print "L" + packagename + "/" + className + ";"+ "->" + item
'''
