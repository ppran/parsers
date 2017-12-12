#This code is useful to generate graphs from logs

import graphviz as gv
import sys
import re

with open(sys.argv[1]) as f:
	text=f.readlines();






#table1=[[]]
processdetails={} # for storing process id and its graph object
lastnode={} # for storing process id and its correspoding last node
i={} # to store counter for edge
j=1
differentid={}
for record in text:
	words = re.split('\s+',record)
	#print words[2] +" " +words[3] +" " +words[7]+" " + words[8] 
	#table1.append([words[2],words[3],words[7],words[8]])
	if words[2] in processdetails:   # if graph bulding already started
		if lastnode[words[2]] != (words[7]+" "+words[8]): #check if previous node is same
			if words[2] == words[3]: # PID = TID
				i[words[2]] = i[words[2]] + 1 
				if words[7] == 'ActivityThread':
					processdetails[words[2]].node(str(i[words[2]]), words[7]+"\\n"+words[8],shape='box')
				else:
					processdetails[words[2]].node(str(i[words[2]]), words[7]+"\\n"+words[8])

				
				
				processdetails[words[2]].edge(str(i[words[2]]-1),str(i[words[2]])) # create edge between previous entry and current
				lastnode[words[2]]= words[7]+" "+words[8] # Add for reference to last added node
				


			else: # Spawned different tid
				if differentid[words[2]] != (words[7]+" "+words[8]): # check if same entry as previous one
					processdetails[words[2]].node(str(j),"TID : "+words[3] +"\\n" + words[7]+"\\n"+words[8])
					processdetails[words[2]].edge(str(i[words[2]]),str(j))
					j=j+1
					differentid[words[2]] = words[7]+" "+words[8]

			
			
			
	else : # if first occurence of process
		
		processdetails[words[2]] = gv.Digraph(format='svg') # start new graph
		lastnode[words[2]] = words[7]+" "+words[8] # Add for reference to last added node
		differentid[words[2]] = words[7]+" "+words[8]
		i[words[2]] = 1
		print record
		print words[7]+" "+words[8]
		processdetails[words[2]].node(str(i[words[2]]),words[7]+"\\n"+words[8],style='filled')
		



for k,v in processdetails.items():
	filename = v.render(filename='img/'+k)
	print filename


	#table1[table1.index(words[2])].teappend(words[2],words[3],words[7],words[8])
	#if words[7] != 'Pranav':
	#	print words
#08-14 11:42:36.720  2844  2844 V Pranav  : TelephonyManager.java getNeighboringCellInfo







'''
g1 = gv.Graph(format='svg')
g1.node('A')
g1.node('B')
g1.edge('A', 'B')
print(g1.source)

filename = g1.render(filename='img/g1')
print filename
'''
