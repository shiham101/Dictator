import os

a=open("index.html","w")

str_html="<html><head></head><body><h1>Index page of Documentation</h1><br><table>"
for path,subdirs,files in os.walk(os.path.dirname(os.path.realpath(__file__))):
	for filename in files:
		if filename not in ["index.html","Index.py","Index.py~"]:
			print filename
			str_html+="<tr><td><a href="+filename+">"+str(filename).split('.m')[0]+"</td></tr>"

str_html+="</table></body></html>"

a.write(str_html)
a.close()