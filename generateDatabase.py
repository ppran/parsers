#this is the code to generate database out of log

import re
import sys


import mysql.connector


#replace user password and database names for you mysql database
cnx = mysql.connector.connect(user='root', password='passwrod_here',database='databasename_here')
if cnx.is_connected():
	print "database connected"
else :
	quit()

cursor = cnx.cursor()


#targetservice = open("testLogParser.txt",'r')
with open("mopub.txt",'r') as f:
	text=f.readlines();

query= "INSERT INTO logdatabase_mopub(logtime,pid,tid,log_tag,hash,b_a,uid,hook_type,associated_activity,class_name,method_name,arguments,return_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
linenumber=0
associated_activity=""

for line in text:
	linenumber= linenumber+1
	print linenumber

	if re.search("ActivityThread123",line):
		time = re.split(' +',line)
		totaltime = time[0] + " " + time[1]
		splitEagleEyeActivity = re.split('EagleEye: ActivityThread123\$\$\$',line)
		splitMore = re.split("\$\$\$",splitEagleEyeActivity[1])
		#print splitMore[0]+":"+splitMore[1]
		#associated_activity
		if (splitMore[0]=="LAUNCH_ACTIVITY") or (splitMore[0]=="RESUME_ACTIVITY"):
			associated_activity = splitMore[1]



	if re.search("Basic",line):


		time = re.split(' +',line)
		#print time[0]
		#print time[1]

		totaltime = time[0] + " " + time[1]
		#print date
		restoftheline = re.split(totaltime,line)
		#print restoftheline
		splitEagleEye = re.split('EagleEye: ',restoftheline[1])
		splitPidTid= re.split(' +',splitEagleEye[0])
		pid = splitPidTid[1]
		tid = splitPidTid[2]
		#if linenumber==444:
		#	print restoftheline
		#	print splitEagleEye
		#	print splitPidTid
		#	print pid
		#	print tid
		

		#print splitEagleEye[1]

		finalSplit = re.split("\$\$\$",splitEagleEye[1])
		hashVal="0"
		uid="0"
		hook_type="0"
		return_value=""

		beforedone= True
		Afterdone=True
		for eac in finalSplit:

			#if linenumber==10433:
			#	print eac + "888"
			if(re.search("Basic",eac)):

				if re.search("BasicSpecialThrough",eac):
					log_tag="BasicSpecialThrough"
					hashVal = "0"
				elif re.search("BasicSpecial",eac):
					log_tag="BasicSpecial"
					hashVal=re.sub("\"","",re.sub("BasicSpecial\":\"","",eac))

				elif re.search("BasicBroadcastSpecial",eac):
					log_tag="BasicBroadcastSpecial"
					hashVal=re.sub("\"","",re.sub("BasicBroadcastSpecial\":\"","",eac))
				elif re.search("BasicCipherSpecial",eac):
					log_tag="BasicCipherSpecial"
					hashVal="0"
				elif re.search("BasicFileSpecial",eac):
					log_tag="BasicFileSpecial"
					hashVal="0"
					hashVal=re.sub("\"","",re.sub("BasicFileSpecial\":\"","",eac))
				elif re.search("BasicURLspecial",eac):
					log_tag="BasicURLspecial"
			
				elif re.search("BasicN",eac):
					log_tag="Basic"
					hashVal=re.sub("\"","",re.sub("BasicN\":\"","",eac))
				else :
					log_tag="Unknown"
					hashVal="0"

			if (re.search("Before",eac)) and beforedone and Afterdone:
				b_a="Before"
				hook_details=re.split(",",re.sub("\]","",re.sub("\"Before\":\[","",eac)))
				uid=re.sub("\"","",hook_details[0])
				hook_type=re.sub("\"","",hook_details[1])
				beforedone=False
			elif re.search("After",eac) and beforedone and Afterdone:
				b_a="After"
				hook_details=re.split(",",re.sub("\]","",re.sub("\"After\":\[","",eac)))
				uid=re.sub("\"","",hook_details[0])
				hook_type=re.sub("\"","",hook_details[1])
				Afterdone=False
			else :
				pass #special case



			if re.search("InvokeApi",eac):
				invoke = re.split(":",eac)
				classmethods=re.split(";->",invoke[1])

				class_name= re.sub("\.","/",(re.sub("\"","",classmethods[0])))
				if class_name[0]!="L":
					class_name= "L"+ class_name
				method_name=re.sub("\"","",classmethods[1])
				arguments = re.sub(invoke[0]+":"+invoke[1],"",eac)

				#for rec in invoke:
				#	print rec

			if re.search("return",eac):
				return_value=re.sub(" \"return\":","",eac)

			if re.search("broadcastReceiver",eac):
				arguments = eac
				
			if re.search("BasicCipherSpecial",eac):
				b_a="NA"
				hook_details1=re.split(",",re.sub("\]","",re.sub("\"BasicCipherSpecial\":\[","",eac)))
				uid=re.sub("\"","",hook_details1[0])
				hook_type=re.sub("\"","",hook_details1[1])

			if re.search("CryptoUsage",eac):
				#class_name="CryptoUsage"
				arguments = eac

			if re.search("CipherAlgorithm",eac):
				#method_name=eac
				return_value=eac


			if re.search("BasicURLSpecial",eac):
				b_a="NA"
				hook_details1=re.split(",",re.sub("\]","",re.sub("\"BasicURLSpecial\":\[","",eac)))
				uid=re.sub("\"","",hook_details1[0])
				hook_type=re.sub("\"","",hook_details1[1])

			if re.search("BasicSpecialThrough",eac):
				b_a="NA"
				hook_details1=re.split(",",re.sub("\]","",re.sub("\"BasicSpecialThrough\":\[","",eac)))
				#print "hook1 : " + hook_details1[0]
				#print "hook2 : " + hook_details1[1]
				uid=re.sub("\"","",hook_details1[0])
				#print uid
				hook_type=re.sub("\"","",hook_details1[1])
				#print hook_type




		args=(totaltime,int(pid),int(tid),log_tag,int(hashVal),b_a,int(uid),hook_type,associated_activity,class_name,method_name,arguments[:499],return_value[:499])
		try:
			cursor.execute(query,args)
		except Exception as e:
			print "linenumber" + str(linenumber)
			print e



cnx.commit()
cursor.close()
cnx.close()


