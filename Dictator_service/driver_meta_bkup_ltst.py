import json
import time
import sys
import msfrpc
import auto_commands
import psutil
import MySQLdb
#import MySQLdb
import threading
import subprocess
import logging
import logging.handlers
import threading
import Auto_logger
import json
import IPexploits
import commands,os
import texttable as tt
import csv
import os
import IPtable
import copy


r = '\033[31m' #red
b = '\033[34m' #blue
g = '\033[32m' #green
y = '\033[33m' #yellow
m = '\033[34m' #magenta
c = '\033[36m' #magenta
p = '\033[95m' #purple
e = '\033[0m' #end
lr= '\033[91m'#Light red


#print "Object created"


class Driver:
	def __init__(self):
		self.con=None
		self.cursor=None
		self.logger=None
		self.Log_file=None
		self.project_id="Default"
		self.lock = threading.Lock()
		self.Auto_logger=Auto_logger.Logger()
		self.commandObj=auto_commands.Commands()
		self.config={}
		self.config_file={}
		self.rows=[]
		self.method_id="INIT"
		self.processed_services=None
		self.commandsJson=None
		self.IPexploits=[]
		self.IPexploit=IPexploits.IPexploits()
		self.IPtable=IPtable.IPtable()
		self.missed_services=None
		self.new_and_unknown=[]
		self.data_path=""
		self.parent_folder="Results_and_Reports"
		self.folder_dir=os.path.dirname(os.path.realpath(__file__))
		results_path=os.path.join(self.folder_dir,"Results")
		#print "\n\nResult path is : "+str(results_path) 
		self.folder_name=os.path.join(results_path,"Data_")
		self.N=10
		self.thread_count=1
		

	def init_connection(self):
		try:
			self.method_id="Init_connection()"
			self.con=MySQLdb.connect("localhost","root","a2mated@P4l4d10n","nmapscan")
			self.cursor = self.con.cursor()
		except Exception,ee:
			self.print_Error("EXception in connection-->"+str(ee))

	def close_connection(self):
		try:
			self.method_id="Close_connection()"
			self.con.close()
		except Exception, ee:
			self.print_Error("EXception in connection-->"+str(ee))

	def parse_and_process(self,mode='c',continue_=False): #note make an entry for service of type unknown in json file and its type would be custom
		try:
			
			self.method_id="parse_and_process()"
			self.print_Log("Starting method --> "+self.method_id)
			self.rows=[]
			self.new_and_unknown=[]
			self.IPexploits=[]
			if (self.missed_services): #check is not none --it returns false for empty isits
				print "Missed services does contain data !!!"
				for k,v in self.missed_services.iteritems():
					entries={}
					entry={}
					service_status='unknown'
					#print "Missed service is "+str(k)
					if (k=='unknown'):
						service_status='unknown'
						entry["unknown"]=True_and_
						entry["new"]=False
						#entry["echo"]=False
					elif(k !=""):
						service_status='new'
						entry["unknown"]=False
						entry["new"]=True
						#entry["echo"]=False
					if entry:
						entries["Entries"]=entry
						entries=json.dumps(entries)
					else:
						entries["Entries"]={"unknown":False,"new":False}
						entries=json.dumps(entries)
					for h_p in v:	
						#print "Appending -->Host-->"+str(h_p[0]) +"Port "+str(h_p[1]) +"Entries :" +str(entries)	
						self.rows.append((self.project_id,str(h_p[0]),str(h_p[1]),str(k),'init',entries,service_status))
						self.IPexploits.append(IPexploits.IPexploits(self.project_id,str(h_p[0]),str(h_p[1]),str(k),'init',entries,service_status))
					
			if (self.processed_services): #dict form of services that are discovered by nmap in dict fom
				#print "1000"
				#print "---->" +str(self.processed_services)
				for k,v in self.processed_services.iteritems():#would always have common services-May also contain custom services
					#print str(k)
					#print "bye"
					entries={}
					commands_and_exploits={}
					row=[]
					service_val=self.commandsJson.get(k) # k would be service and would act as key for commandsjson
					#all_commands=service_val.get('Commands') #commands is  list of dictionaries
					is_custom=service_val.get('Custom')
					#print "here reached"
					if(is_custom==False):
						entries=self.getTemplate(k)
						#print "entries are -->" +str(entries)
						if(entries != -1):
							#print "here reached also 1.2\n
							for h_p in v:	
								self.rows.append((self.project_id,str(h_p[0]),str(h_p[1]),str(k),'init',entries,'existing'))
								self.IPexploits.append(IPexploits.IPexploits(self.project_id,str(h_p[0]),str(h_p[1]),str(k),'init',entries,'existing'))
								self.config[k]=row
						else:
							print "Error entry -1 for key -- Does not support recursive classes:"+str(k)
							self.print_Error("Entry error (returns -1) for key "+str(k))

					elif(is_custom==True):
						all_commands=service_val.get('Commands')
						if all_commands:
							for entry in all_commands : #each command entry will pint to a custom class
								if (entry):
									entries=self.getTemplate(entry)
									if(entries != -1):
										for h_p in v:	
											#self.rows.append((self.project_id,str(h_p[0]),str(h_p[1]),str(k),'init',entries,'existing'))
											self.rows.append((self.project_id,str(h_p[0]),str(h_p[1]),str(entry),'init',entries,'existing'))
											self.IPexploits.append(IPexploits.IPexploits(self.project_id,str(h_p[0]),str(h_p[1]),str(entry),'init',entries,'existing'))
											self.config[k]=row
							

			if self.rows:
				#print "\n\n\nrows are \n\n"
				#print str(self.rows)
				#print "1"
				#self.makeBulkEntries(self.rows)
				self.IPexploit.insertIPexploits(self.rows)
				print "\n"
				print r+"{+}______________Launching with selected configuration !!!__________________"+e
				if mode=='c':
					self.launchConfiguration()	
				else :
						if continue_== False:
							return_val=self.launchConfiguration(False,'gui',False)
							return return_val
							#make_config=False,mode='c',choice='1',continue_=False):
						else: #no need for follwoing.It will be executed from main only
							val=self.launchConfiguration(True,'gui',True) #overwrite=true and continue=true
							if val==1:
								self.launchExploits()
							else:
								print "\n\n Some massive error occured --I am here !!"
							#self,make_config=False,mode='c',continue_=False)
			else :
				print "\n"+g+"No Common service and no unknown or new service discovered !!"+e
				return_set={}
				return_set["status"]="empty"
				return_set["value"]="No Common service and no unknown or new service discovered !!"
				return return_set
				#self.launchConfiguration()
				
		except Exception, ee:
			self.print_Error("EXception -->"+str(ee))
	
	def DrawTable(self,records,header=[],col_width=[]):
		tab = tt.Texttable()
		x = [[]]
		for row in records:
	   		x.append([str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[7])])
		tab.add_rows(x)
		tab.set_cols_align(['r','r','r','r','r','r'])
		if (header):
			tab.header(header)
		else:
			tab.header(['ID','PROJECT_Id','HOST','PORT','SERVICE','SERVICE TYPE'])
		if (col_width):
			tab.set_cols_width(col_width)
		print tab.draw()

	def getTemplate(self,service,reconfig=False):
		#print "\n\nObtaining template\n\n "
		entries={}
		commands_and_exploits={}
		row=[]		
		service_val=self.commandsJson.get(service)
		if(service_val):
				all_commands=service_val.get('Commands')
				if all_commands:
					for entry in all_commands :
						if entry:
							method_name=entry.get('method')
							command_id=entry.get('id')
							commands_and_exploits[command_id]=[True,"0","0"]
						else:
							return -1
											
					entries["Entries"]=commands_and_exploits
					entries=json.dumps(entries)
					return entries
				else:
					return -1
			
		else :
			#if(reconfig==True):
			print r+"[*] Invalid choice Enter a valid service class as per master json "
			return -1
	
	def InsertAdditionalServices(self,unKnownServices,id_list):
		self.method_id="InsertAdditionalServices()"
		self.print_Log("Started method InsertAdditionalServices()")
		while (1):
				pass_check=True
				try:
					choice=raw_input( "\n\n"+y +">Press 1 to add additional test case and press 2 to proceed"+e)
					if (choice =="2"):
						break
					elif (choice=="1"):
						
						print b +"\n>Enter Host port and service in single line seperated by comma "+e
						print y +"[+] Eg: 192.168.179.136,80,ssh \n"+e
						entry=raw_input(y+">")
						line=entry.split(',')
						if (len(line) !=3):
							print "\n" +r+"[+] Invalid Choice "+e
							continue
						#(Pid,Host,Port,Service,Project_status,Exploits)
						ip=str(line[0])
						ip_chk=ip.split('.')
						if(len(ip_chk) < 2) :
							pass_check=False
							print "\n"+r+"[*]-Invalid Host "+e
							continue;
						if((str(line[1]).isdigit())==False):
							pass_check=False
							print "\n"+r+"[*]-Invalid PORT"+e
							continue
						service_val=self.commandsJson.get(str(line[2]))
						if (not service_val):
							print "\n"+r+"[*]--------Invalid SERVICE"+e
							continue
						all_commands=service_val.get('Commands')
						is_custom=service_val.get('Custom')
						if (is_custom==False):
							json_template=self.getTemplate(line[2],True)
							if (json_template ==-1):
								pass_check=False
								print "\n"+r+"[*]-Invalid SERVICE"+e
								continue
						
							if(pass_check==True):	
							
								print b+"json template--> " +str(json_template)
								if (json_template !=-1):
									row=(int(self.project_id),line[0],line[1],line[2],'init',json_template,'existing')
									self.IPexploit.insertIPexploits(row,True)
									print "\n"+y+"[+]The reconfiguration has been saved "+e
								else:
									print "\n"+r+"[*] Service class invalid "+e
							else:
								print "\n\n"+g+"[*]**********"+r+"Correct the errors and reenter"+g+"*********"+e+"\n\n"	
						elif (is_custom==True):
								if all_commands:
									for entry in all_commands : #each command entry will point to a custom class
										if (entry):
											json_template=self.getTemplate(entry,True)
											if (json_template ==-1):
												pass_check=False
												print "\n"+r+"[*]-Invalid SERVICE"+e
												continue
						
											if(pass_check==True):	
							
												print b+"json template--> " +str(json_template)
												if (json_template !=-1):
													row=(int(self.project_id),line[0],line[1],str(entry),'init',json_template,'existing')
													self.IPexploit.insertIPexploits(row,True)
													print "\n"+y+"[+]The reconfiguration has been saved "+e
												else:
													print "\n"+r+"[*] Service class invalid "+e
											else:
												print "\n\n"+g+"[*]**********"+r+"Correct the errors and reenter"+g+"*********"+e+"\n\n"
										else:
											print "\n\n"+g+"[*] **Some issue with master json..Contains no entry for this service for commands"+e
								else:
									print "\n\n"+g+"[*] **Some issue with master json..Commands key missing"+e
						else:
							print "\n\n"+g+"[*] **Some issue with master json..Custom flag not set"+e
										
				except Exception ,ee:
					print "Exception occured :" +str(ee)
					self.print_Error("Exception occured "+str(ee))
		self.method_id="InsertAdditionalServices()"
		self.print_Log("Stopped method InsertAdditionalServices()")


	def UpdateUnknownServices(self,unKnownServices,id_list,unknownservice_json):
		self.method_id="UpdateUnknownServices()"
		self.print_Log("Started method UpdateUnknownServices")
		if (unKnownServices):
			update_entries=[]
			invalid=False
			while (1):
				try:	
					invalid=False
					reconfig=False
					choice=raw_input("\n"+b +">Press 1 to reconfigure press 2 to Launch Tests"+e)
					if (choice =="2"):
						break
					elif(choice=="1"):
						rec_id=raw_input( b +"Enter the Id of the record to reconfigure "+e)
						if rec_id in id_list:
							pass_check_=True
							reconfig=True
							update_entry={}
							update_entry["id"]=str(rec_id)
					
							inp=raw_input("Enter 1 to reconfigiure service and 2 to reconfigure all <host,port and service> ")

							if(inp=="1"):
								print y+"You may reffer to servics.txt file present in the parent folder to see the list of services currently supported"+e
								service_name=raw_input ("\n\n"+b +"Enter new service for the record id to be updated \n"+e)
								print "chosn service -->"+str(service_name)
								service_val=self.commandsJson.get(service_name) 
								print "service_val is :"+str(service_val)
								if (not service_val):
									print "\n"+r+"[*]-------Invalid SERVICE--------------"+e
									pass_check_=False
									continue
								all_commands=service_val.get('Commands') #commands is  list of dictionaries
								is_custom=service_val.get('Custom')
			
								if(is_custom==False):
										json_template=self.getTemplate(service_name,True) #this service would be added by user and 
										if (json_template ==-1):
											pass_check_=False
											print "\n"+r+"[*]-Invalid SERVICE"+e
											continue
										
						
										if( (pass_check_==True)):
											
											update_entry["service"]=service_name.lstrip().rstrip()
											update_entry["pid"]=str(self.project_id)
											print "\n\n[+]Updating the record!!"
											self.IPexploit.Update_Reconfig(update_entry["id"],update_entry["pid"],'','',update_entry["service"],'existing',json_template,True)
											print "\n\n"+g+"[+]Record Updated!!"+e


								elif((is_custom==True) and (all_commands)):
									print r+"\n\n[+]You have selected a custom class option.A custom class can be configured by selecting <configure all> option from the last menu.KIndly set custom service from there "+e
									continue
				
									
							elif(inp=="2"):
								print b +"Enter host port and service in single line seperated by comma "+e
								print y +"Eg: 192.168.179.136,80,ssh "+e
								entry=raw_input(y+">")
								line=entry.split(',')
								if (len(line) !=3):
									print "\n" +r+"[+] Invalid Choice "+e
									continue
								ip=str(line[0])
								ip_chk=ip.split('.')
								if(len(ip_chk) < 2) :
									pass_check_=False
									print "\n"+r+"[*]-Invalid Host "+e
									continue
								if((str(line[1]).isdigit())==False):
									pass_check_=False
									print "\n"+r+"[*]-Invalid PORT"+e
									continue
								service_val=self.commandsJson.get(str(line[2])) 
								print "The service val is -->"+str(service_val)
								if (not service_val):
									print "\n"+r+"[*]-------Invalid SERVICE--------------"+e
									pass_check=False
									continue
								all_commands=service_val.get('Commands') #commands is  list of dictionaries
								is_custom=service_val.get('Custom')
			
								if(is_custom==False):
										json_template=self.getTemplate(line[2],True) #this service would be added by user and 
										if (json_template ==-1):
											pass_check_=False
											print "\n"+r+"[*]-Invalid SERVICE"+e
											continue
										
						
										if((reconfig) and (not invalid) and (pass_check_==True)):
											update_entry["host"]=str(line[0]).lstrip().rstrip()
											update_entry["port"]=str(line[1]).lstrip().rstrip()
											#check weather the service added is there in the  master json
											update_entry["service"]=str(line[2]).lstrip().rstrip()
											update_entry["pid"]=str(self.project_id)
											print "\n\n[+]Updating the record!!"
											self.IPexploit.Update_Reconfig(update_entry["id"],update_entry["pid"],update_entry["host"],update_entry["port"],update_entry["service"],'existing',json_template)
											print "\n\n"+g+"[+]Record Updated!!"+e


								elif((is_custom==True) and (all_commands)):
									insert_entries=[]
									made_insertion=False
									parent_service =unknownservice_json.get(str(update_entry["id"]))
									print r+"[+]Parent service to be updated is -->"+str(parent_service)+e
									for entry in all_commands : #each command entry will point to a custom class
										if (entry):
											json_template=self.getTemplate(entry,True)
											if (json_template ==-1):
												pass_check_=False
												print "\n"+r+"[*]-Invalid SERVICE"+e
												continue
											
											if((reconfig) and (not invalid) and (pass_check_==True)):
												update_entry["host"]=str(line[0]).lstrip().rstrip()
												update_entry["port"]=str(line[1]).lstrip().rstrip()
												#check weather the service added is there in the  master json
												#update_entry["service"]=parent_service
												update_entry["service"]=entry
												update_entry["pid"]=str(self.project_id)
							
												print "\n\n[+]Updating the record!!"
												row=(int(self.project_id),update_entry["host"],update_entry["port"],update_entry["service"],'update',json_template,'existing')
												self.IPexploit.insertIPexploits(row,True)
												made_insertion=True
												print "\n\n"+g+"[+]Record Updated!!"+e
									if(made_insertion):
										self.IPexploit.removeIPexploit(int(update_entry["id"]))
										self.print_Log("Details updated for custom added service !!")
										print "\n\n"+g+"[+] Details updated Successfully for current service "	+e
							
							else:
								print r+"\n[+] INvalid choice \n"+e
								continue	
						else:
							print r +"[*][*]In valid Id-->Enter a valid ID\n" +e
							#invalid=True
							continue

				except Exception ,ee:
					self.print_Error("Exception in Update unknown services --" +str(ee))
					print ("Exception in update unknown services --"+str(ee))
							
		else :
			print g+"\n[+] No UNknown services were detected"+e

		self.method_id="UpdateUnknownServices()"
		self.print_Log("Stopped method UpdateUnknownServices")


	def reConfigure(self,mode='c'):
		try:
			self.method_id="Reconfigure()"
			self.print_Log("Started method Reconfigure")
			unKnownServices=self.IPexploit.getUnknownServices(self.project_id)
			id_list=[]
			
			repeat=1
			unknownservice_json={}
			if unKnownServices:
				print "found unknown services !!!"
				for entry in unKnownServices:
					id_list.append(str(entry[0])) #the one's having service type as unknown
					unknownservice_json[str(entry[0])]=str(entry[4])
				print y +"[+]" + "Discovered some unknown and new  services--Configure them or exploits woould not be launched against them" +e
				print "\n"
				self.DrawTable(unKnownServices)
				return_set={}
				return_set["services"]=unKnownServices
				if mode=="c":
					self.UpdateUnknownServices(unKnownServices,id_list,unknownservice_json)
				#else:
					

			self.InsertAdditionalServices(unKnownServices,id_list)
	
			#print "Press 1 to launch exploits and 2 change master file and  exit :"
			choice="0"
			while(1):
				choice=raw_input("\n"+g+"[+]Press 1 see the updated configuration and launch exploits and 2 change master file and  exit :\n"+e)
				if((choice=="1") or(choice=="2")):
					break
				else:
					print "\n"+r+"[*] Choice invalid \n"+e
			self.method_id="Reconfigure()"
			self.print_Log("Ending method Reconfigure()")
			if (choice =="1"):
				self.launchConfiguration(True)
				#self.launchExploits()
				#self.print_Log("Ended method Reconfigure")
			else :
				return


		except Exception,ee:
			self.print_Error("Error occured !!:" +str(ee))
	
	def makeConfigurationFile(self):
		config_file=str(self.project_id)+"Config.json"
		config_file_path = os.path.join(self.data_path, config_file)
		with open(config_file_path, 'w') as outfile:
     			json.dump(self.config_file, outfile, indent = 2,ensure_ascii=False)


	def launchConfiguration(self,make_config=False,mode='c',continue_=False):
		try:
			print "\n"+g+"[+] Launching configuration ...."+e
			#self.init_connection()
			self.method_id="launchConfiguration()"
			self.print_Log("Starting method --> "+self.method_id +"Project id --> "+self.project_id)
			id_=int(self.project_id)
			IPexploits=self.IPexploit.getIpExploits(self.project_id)
			IPexploits_and_commands=[]
			list_row=[]
			config_list=[]
			tab_draw=[]
			for row in IPexploits: #row is of type tuple whic is read only
				
				#print str(row[4])
	   			commands=self.getCommands(row[4],row[2],row[3])#x.append([str(row[0]),str(row[1])])
				#print" commands got are :" +str(commands)
				list_row.append((row[0],row[1],row[2],row[3],row[4],row[5],commands))
				tab_draw.append((row[0],row[1],row[2],row[3],row[4],row[5],'',commands))
			#note list row will have all the details required to be returned
	
			#print tab.draw()
			header=[]
			header=['ID','PROJECT_Id','HOST','PORT','SERVICE','Commands']
			col_width=[5,5,15,5,7,40]
			#self.DrawTable(tab_draw,header,col_width)
			return_set={}
			

			if mode !='c' and continue_== False:
				all_exploits=self.IPexploit.getUnknownServicesOnly(self.project_id)
				for row in all_exploits: #row is of type tuple whic is read only
					empty_dict={}
					empty_dict["status"]="empty"
					list_row.append((row[0],row[1],row[2],row[3],row[4],row[5],empty_dict))
				return_set["status"]="reconfig"
				return_set["value"]=list_row
				return return_set

			for row in list_row:
				config_entry={}
				print "\n"+ lr +"######################################################################################"+e
				#print str(row)
				print ("\n"+g+"[+]Project id : "+y+str(row[1])+g+" [+] Host : "+y+ str(row[2])+g+" [+] Port : "+y+str(row[3]) +g+" [+] Service : "+y+str(row[4])+e)
				#print "Commands :"
				command_data=row[6]
				config_entry["id"]=str(row[0])
				config_entry["Project_id"]=str(row[1])
				config_entry["Host"]=str(row[2])
				config_entry["Port"]=str(row[3])
				config_entry["Service"]=str(row[4])
				config_entry["IsCustom"]=False
				config_entry["IsModified"]=False
				command_list=[]
				print "\n"
				for k in command_data:
					id_=k.get("id")
					command_list.append(id_)
					print b+"*************************************************"+e
					print r+"Command id :-->"+y+str(id_)+e
					args=k.get('args')
					print r+"Commands :"+e
					for aur in args:
						if isinstance(aur, basestring):
							aur=aur.replace('\n','')
						print str(aur)
					print b+"*************************************************"+e
				#print "\n"
					
				print "\n"+ lr +"######################################################################################"+e
				config_entry["Commands"]=command_list
				config_list.append(config_entry)
			self.config_file["Records"]=config_list

			if mode !='c' and continue_==True and make_config==True:
				self.makeConfigurationFile()
				return 1

			if(make_config==True):
				self.makeConfigurationFile()
			
			print y+"\n\n[+] The above configuration has been selected :Press 1 tolaunch the tests ,2 to reconfigure !!!"+e
			choice="0"
			if mode=='c':
				while (1):
					choice =raw_input(b+"\n>Please enter your choice\n "+e)
					if((choice=="1") or (choice=="2")):
						break;
					else:
						print "\n" + r +"[+] Invalid choice " +e

				if (choice =="1"):
				
					self.launchExploits()
				else :
					self.reConfigure()
			else:
					print "Some error occured with flow.This should not be executed !!"
					#self.reConfigure("gui")
					

		except Exception ,ee:
			self.print_Error("EXception 11-->"+str(ee))

	def getCommands(self,k,host,port):
		try:
			# "In get commands"
			#print str(k)
			service_val=self.commandsJson.get(k)
			#print "Got commands"
			#print str(service_val)
			all_commands=service_val.get('Commands')
			#print "here"
			arg_list=[]
			#arg_list.append(1)
			for arg in all_commands :
				#print str(args)
				if isinstance(arg, basestring):
						arg=arg.replace("<host>",host)
						arg=arg.replace("<port>",port)
				arg_list.append(arg)


			return arg_list

		except Exception, ee:
			self.print_Error("EXception -22->"+str(ee))
			return -1
	
		



	def set_log_file(self):
		self.Log_file=str(self.project_id) +str("_Log_file_info.txt")
		print "\n\n\nData path is -->"+str(self.data_path) 
		self.Log_file_path = os.path.join(self.data_path, self.Log_file)
		print "Log file is --> " +str(self.Log_file)+"and log file path is : "+str(self.Log_file_path)
		print "\n@@@@\n"
		#self.Log_file=str(self.project_id) +str("_Log_file_info")
		self.logger=self.Auto_logger.configureLoggerInfo(self.method_id,self.Log_file_path)	
		self.print_Log("\n\nStarting \n\n")
		time.sleep(3)
		print "hello !!!  Logger is set"

	def init_project_directory(self):
		print "Initialising parent directory "
		try:
			if not os.path.exists(self.folder_name+str(self.project_id)):
				#print "Making directory !! folder name is"+str(self.folder_name)
				#self.print_Log("Making project directory !")
				os.mkdir(self.folder_name+str(self.project_id))
				#print "hhh"
			self.data_path=self.folder_name+str(self.project_id)
			return 1;
		except Exception ,ee:
			#self.print_Error("Error while creating directory !!"+str(ee))
			print "EX "+str(ee)
			return -1
	

	#def main_gui(self,project_id=''):
			
	def main(self,mode='c',project_id_='',continue_=False,delete=False,get_updated_config=False,threading_=False,concurrent=False):
		try:
			return_set={}
			self.method_id="Main()"
			
			tab = tt.Texttable()
			x = [[]]
			#self.init_connection()
			self.project_obj=IPtable.Projects()
			#result = self.cursor.execute("SELECT id, projects from project where project_status='complete'")
			#result=self.cursor.fetchall()
			result=self.project_obj.completed_projects()
			valid_projects=[]
			for row in result:
	   			x.append([str(row[0]),str(row[1])])
				valid_projects.append(str(row[0]))

			tab.add_rows(x)
			tab.set_cols_align(['r','r'])
			tab.header(['IDs','PROJECT_NAME'])
			#if mode =='c':
				

				#print "\n"
			if mode=='c':
				print r+"List of Project with IDs"+e +"\n"
				print tab.draw()
				while 1:
					id = raw_input(b+"[+]Enter The Project Id For Scanning :\n>"+e)
					reenter=False
					if id in valid_projects:
						#print "yes"
						check_status=self.IPexploit.Exists(id)
						#print "here"
						print check_status
						if (check_status ==1):
							print y+"[+] It seems ,you have alreday launched exploits for this project .\n[+]Proceeding further would overwrie old logs."+e	
							while(1):
								ch=raw_input(b+"[+]Press 1 to Proceed 2 to Re enter.\n"+e)
								if ch=="1":
									self.IPexploit.removeIPexploit(id,all_=True)
									break
								elif ch=="2":
									reenter=True
									break
						if (reenter==False):		
							break
					else:
						print r+"[+] Invalid project id.Please select an id from the provided list "+e
						print "\n"
			else:
				id=project_id_
				print "\n\n Project id is :	"+str(id)+"\n\n"  
				if id in valid_projects:
						#print "yes"
						check_status=self.IPexploit.Exists(id)
						#print "here"
						print check_status
						if (check_status ==1):
							if(get_updated_config==False) and (continue_==False):
						
								if(delete==False):
									return_set["status"]="exists"
									return_set["value"]="It seems ,you have already launched exploits for this project .Proceeding further would overwrie old logs.Do you wish to continue"
									return return_set;
								elif(delete==True) and (continue_==False) and (concurrent==False): #launching get req second time
									print "About to remove entries even when status =false !!"
									self.IPexploit.removeIPexploit(id,all_=True)
								
				else:
						return_set["status"]="failure"
						return_set["value"]="Invalid project id.Please select an id from the provided list"
						print r+"[+] Invalid project id.Please select an id from the provided list "+e
						print "\n"
						return return_set

			self.project_id=id
			#print "Removed !!"
			#print "-1"
			status=self.init_project_directory()
			print "INitialised"
			if (status==-1):
				return_set["status"]="failure"
				return_set["value"]="some error occured while creating the directory--Exiting..."
				print("some error occured while creating the directory\nExiting...")
				if mode !='c':
					return return_set
				else:
					return
			self.set_log_file()
			self.IPexploit.data_path=self.data_path
			self.IPexploit.logger=self.logger
			self.commandObj.project_id=self.project_id
			self.commandObj.data_path=self.data_path
			self.commandObj.set_log_file()
			self.commandObj.logger_info=self.logger
			
			self.print_Log("\n\n\nWelcome  STARTING MAIN METHOD OF DRIVER FILE FOR PROJECT ID --> " +str(id))
			lst1 = []
			###very importent -->check here weather the selected id from user actually falls under completed projects"
			id_=int(id)
			if 1:#(get_updated_config==False): #Must exe for both exploit launching and def config
				self.init_connection()
				result_ = self.cursor.execute("SELECT Sevices_detected from IPtable_history where project=%s and Sevices_detected is not null",(id_,))
				self.close_connection()
				result_=self.cursor.fetchall()
				print "Hello"
				for row in result_:
					if row[0] is not None:
						string = str(row[0])
						s = string.split("\n")
						for k in s:
							t = str(k).split(";")
							lst1.append(t)
				#print "List 1 -->"+ str(lst1)
				lst = {}

				for i in lst1:
					if len(i) is not 1:
					 #print i[0]
					 temp={i[3]:[i[0],i[2]]}
					 if cmp(lst.keys(), temp):
						lst.setdefault(i[3], []).append([i[0],i[2]])
					 else:
						lst.update(temp)

				lst.pop("name") #-->All service and val disc by nmap  {ssh:[[h1,p1],[h2,p2]],ftp--}
				all_config_file=os.path.join(self.folder_dir,"all_commands.json")
				with open(all_config_file,"rb") as f:
					jsonpredata = json.loads(f.read()) #--> all service types in master json 

				lst_pre = jsonpredata.keys()
				lst_temp = lst.keys()
				ss = set(lst_temp).intersection(set(lst_pre)) #-->All services common to what is discovered by nmap and what is there in master json-->it will skip the use case if nmap identifies a service that our master json would not have.Thus it would be good to do a set difference as well suc that all the services that are discovered by nmap and are not there in master json would be fetched
				ms=list(set(lst_temp) - set(lst_pre))

				print "ss is " +str(ss)
				dic = {}
				for i in ss:
					for k in lst.get(i):
						dic.setdefault(i, []).append(k)#thus all refined data would be in dic.All services and host,ports that ar discovered by the nmap scan placed like {ssh:[[h1,p1],[h2,p2]],ftp--}
					#dic.update({i:k for k in lst.get(i)})
				ms_dic={}
				for i in ms:
					for k in lst.get(i):
						ms_dic.setdefault(i, []).append(k)
				print "here reached "
				self.processed_services=dic #--Processed services would now contain relevent json 
				self.commandsJson=jsonpredata #all data from json file is in commandsjson
				self.missed_services=ms_dic

			if mode=='c':
				self.parse_and_process()
			else:
				#print "value of continue is :"+continue_
				#bool_=False
				#print "bool value :"+bool_
				if continue_==False and get_updated_config==False:#Initial run to get default config
					return_val=self.parse_and_process(mode,continue_)
					return return_val
				elif continue_==False and get_updated_config==True:
					return_val=self.launchConfiguration(False,'gui',False)
					return return_val
				elif continue_==True and get_updated_config==False:#when -->for launching exploits
					print "\n\nLaunching config \n\n"
					val=self.launchConfiguration(True,'gui',True) #To mk config file overwrite=true and continue=true (self,make_config=False,mode='c',continue_=False):
					print "Val ret is :"+str(val)
					if val==1:
						print "Now Launching exploits !"
						if threading_==False:
							self.launchExploits()
							print "Launched Exploits !"
						else:
							active_threads=threading.enumerate()
							counter=len(active_threads)
							print "\n---\nMain At the begining --1---- the active threads are :---"+str(active_threads)+"\n---\n\n"
							self.thread_count=counter

							self.startProcessing(self.N)
							time.sleep(100)
							# "**Pooling started **\n"
							active_threads=threading.enumerate()
							counter=len(active_threads)
							print "\n---\nMain At the begining the active threads are :---"+str(active_threads)+"\n---\n\n"
							self.thread_count=counter
							self.method_id="Main()"
							self.print_Log("**Pooling started :**")
							self.start_Polling()
						if threading_==True:
							self.check_final_status()
						else:
							self.IPexploit.UpdateProjectStatus('complete',self.project_id)	
						return_val={}
						return_val["status"]="success"
						return_val["value"]="Project execution finished"
						#return return_val
					else:
						return_val={}
						return_val["status"]="failure"
						return_val["value"]="Some error occured.It occured while Launching configuration."
						return return_val
						print "\n\n Some massive error occured --I am here !!"

					#self.parse_and_process(mode,continue_)
			print "Reached here !!"
			if(self.generate_report==True):
				if mode=='c':
					while (1):
						inp=raw_input("\n" + g +"[+] Press 1 to generate the report and 2 to exit \n")
						if (inp=="1"):
							self.IPexploit.generate_report(self.project_id)
							break
						elif(inp=="2"):
							break
				else:
					self.IPexploit.generate_report(self.project_id)
						
			temp_file=str(id) + "_result_data.txt"
			data_file=os.path.join(self.data_path,temp_file)
			json.dump(dic,open(data_file,"wb"))
			data = json.load(open(data_file,"rb"))

			data_temp = []
			for j in data:
			    data_temp.append(j) #all keys of json file go in data_temp
	
		except Exception ,ee:
			print str(ee)
			self.print_Error("Error occured in Main method "+str(ee))
		

	def check_final_status(self):
				th_count=threading.enumerate() 
				print "# of threads Alive are :"+str(len(th_count))
				#while (1) :
				if 1:
					if (len(th_count)==1):
						print "\nNow stopping and saving Global Project Id : "+ str(self.project_id)+"\n";	
						#global self.CURRENT_PROJECT_ID
						if 1:#((self.CURRE != "") and (self.CURRENT_PROJECT_ID is not None)):
							status=self.IPexploit.checkStatus(self.project_id)
							if(status):
								processing_status=status[0]
								pause_status=status[1]
								if((processing_status) and (not (pause_status))):#will just check once
										print "Still left with some hosts that display status as processing !!!"
										time.sleep(10)#the reason for this delay is suppose some thread is fired but not scheduled yet and thus the status would show as incomplete and if we immidiately statprocessing,then 2 threads might point to 1 record
										self.startProcessing(self.N)
										print "Main Thread--->Again Starting pooling in 50 sec :"
										time.sleep(50)
										print "Polling started-->again :"
										self.start_Polling()
										#xx=2
								if ((not(processing_status))  and (not(pause_status))): #to update status from incompl to comp								
									print "Launching clear logs and finally closing !!!"
									self.IPexploit.UpdateProjectStatus('complete',self.project_id)
									#self.IPtable.clearLogs(self.CURRENT_PROJECT_ID,'complete')
								#else :
									#clearLogs(self.CURRENT_PROJECT_ID,'complete')
				#end_time = time.time()
				#print "Time taken in seconds : "+str(end_time-start)


	def print_Log(self,message):
		
		try:
			print "Printing to log "
			self.lock.acquire()
			self.logger.debug(message)
			self.lock.release()	
			print "Printed to log"
		except Exception ,ee:
			self.lock.acquire()
			self.logger.critical(message +"--Exception :  --"+str(ee))
			self.lock.release()
		print message+"\n"

	def print_Error(self,message):
		try:
			self.lock.acquire()
			self.logger.error(message)
			self.lock.release()
		except Exception ,ee:
			self.lock.acquire()
			self.logger.error(message +"--Exception :  --"+str(ee))
			self.lock.release()
		print message+"\n"
	
	
	def startProcessing(self,n):
	 try :
			active_threads=threading.enumerate()
			counter=len(active_threads)
			print "\n---\nB4 start processing --  the active threads are :---"+str(active_threads)+"\n---\n\n"
							#self.thread_count=counter

			self.method_id="LaunchExploits() with Threading"
			self.print_Log("Started method LaunchExploits()")
			self.generate_report=True
			All_services_and_hosts=self.IPexploit.getIpExploits(self.project_id,n)
			if (All_services_and_hosts):
				self.StartThreads(All_services_and_hosts)			
			else :
				return;
	 except Exception ,ee :
		print "Exception 12 " +str(ee)	

	def getPausedStatus(self,project_id):
		try :
			status=self.IPexploit.getStatus(project_id)
			return status
		except Exception ,ee:
			print "Exception getstatus " +str(ee)
			return 0


	def start_Polling(self):
		try:
			stop_db_poll=False #use this logic to stop unnecessary db poll when all hosts finish
			#global N
			while 1:
				time.sleep(5)
				active_threads=threading.enumerate()
				counter=len(active_threads)
				#=1
				print "Parent thread count oreginally was :"+str(self.thread_count)
				print "Polling --> Threads remaining are :"+str(active_threads)+"\n"
				
				if(counter==self.thread_count):
						status=self.IPexploit.checkStatus(self.project_id)
						if(status):
							processing_status=status[0]
							pause_status=status[1]
							if((processing_status) and (not (pause_status))):#will just check once
									print "Still left with some records that display status as processing or incomplete "
									time.sleep(10)
									self.startProcessing(self.N)
									time.sleep(50)
							else:		
									
								print "Active Threads are only 1 --Scan about to finish --Threads remaining are :"+str(active_threads)
								self.print_Log("Active Threads are only 1 --Scan about to finish --Threads remaining are :"+str(active_threads))
								break;

				elif(counter <=(self.N+1)):
					if(not(self.getPausedStatus(self.project_id))):
						limit=(self.N+1)-counter
						if(limit != 0): 
							left_hosts=self.startProcessing(limit) 
							time.sleep(1)	
						else: #some thread is being executed
							time.sleep(2) #All threads are running ,just wait for 1 sec and then pool again	
							
					else:
						time.sleep(10) #status --> pause then it would get terminated on its own by kill
				else :
					print "\n\n\n\n------FATEL ERROR-------\n\n\n"
					print "Number of threads cant exceed : "+str(self.N+1)
					
							
			
		except Exception ,ee:
			print "Exception caught 15" +str(ee)



	def StartThreads(self,IPexploits_data):
		try:
			self.method_id="Start Threads"
			threads=[]
			self.print_Log("Starting : "+str(len(IPexploits_data)) +"Threads for services :" )
			for exploit in IPexploits_data:
						current_record_id=exploit[0]
						service=str(exploit[4])
						host=exploit[2]
						port=exploit[3]
						self.print_Log("Service,Host,port  is -->"+str(service)+"  " +str(host)+"  "+str(port))
						entry=self.commandsJson.get(service)
						meta=entry.get('Commands') 
						lk= threading.enumerate()
						if len(lk)<(self.N+1) :	
							print "Copying object !"
							obj=Driver()
							obj.con=self.con#=None
							obj.cursor=self.cursor#=None
							obj.logger=self.logger#=None
							obj.Log_file=self.Log_file#=None
							obj.project_id=self.project_id#="Default"
							obj.lock=self.lock #= threading.Lock()
							obj.Auto_logger=self.Auto_logger#=Auto_logger.Logger()
							obj.commandObj=auto_commands.Commands()#=THis line causes the bug /issue 
							obj.commandObj.project_id=self.project_id
							obj.commandObj.data_path=self.data_path
							obj.commandObj.set_log_file()
							obj.commandObj.logger_info=self.logger
							obj.config=self.config#={}
							obj.config_file=self.config_file#={}
							obj.rows=self.rows#=[]
							obj.method_id=self.method_id#="INIT"
							obj.processed_services=self.processed_services#=None
							obj.commandsJson=self.commandsJson#=None
							obj.IPexploits=self.IPexploits#=[]
							obj.IPexploit=self.IPexploit#=IPexploits.IPexploits()
							obj.IPtable=self.IPtable#=IPtable.IPtable()
							obj.missed_services=self.missed_services#=None
							obj.new_and_unknown=self.new_and_unknown#=[]
							obj.data_path=self.data_path#=""
							obj.parent_folder=self.parent_folder#="Results_and_Reports"
							obj.folder_dir=self.folder_dir#=os.path.dirname(os.path.realpath(__file__))
							#obj.results_path=results_path=os.path.join(self.folder_dir,"Results")
							#print "\n\nResult path is : "+str(results_path) 
							obj.folder_name=self.folder_name
							obj.N=self.N
							

							#obj=copy.deepcopy(self)	
							print "Object copied !"
							print "New object instance is :"+str(obj) +" and the main object instance is :"+str(self)	
							
							t = threading.Thread(target=obj.launchThread,args=(meta,host,port,service,current_record_id)) 
							try :
								self.IPexploit.UpdateStatus('processing',host,port,int(self.project_id),int(current_record_id))
							except Exception, ee:
								print "EXception while updating status : " +str(ee)				
							#threads.append(t)
							t.start()
							obj.print_Log("\nStarted thread --"+str(t)+"--- for IP :"+str(host) + " Port : "+  str(port)+" and service : "+str(service))
							time.sleep(3)
		except Exception ,ee:
			print ("Inside exception of start Threads ! " +str(ee))


	def launchThread(self,meta,host,port,service,current_record_id):
					try :
						print "The thread is invoked with innstance :"+str(self)
						for entries in meta :
							method_name=entries.get('method')
							args=entries.get('args')
							self.commandObj.method_id=method_name
							self.commandObj.command_id=entries.get('id')
							self.commandObj.current_record_id=current_record_id
							self.commandObj.current_host=host
							self.commandObj.current_port=port
							self.commandObj.data_path=self.data_path
							final_args=[]
							for arg in args:
								if isinstance(arg, basestring):
									arg=arg.replace("<host>",host)
									arg=arg.replace("<port>",port)
								final_args.append(arg)
							if ((method_name)):
								func = getattr(self.commandObj,method_name)
								print "Invoking !!! with instance -->"+str(self)
								is_interactive=entries.get('interactive')
								self.commandObj.print_Log_info("\n\n\n STARTING EXPLOITS  FOR PROJECT ID --> " +str(self.project_id)+" with object instance --"+str(self))
								print "Logged"
								if((is_interactive !=None ) and (is_interactive =="1")):
									print "Launching General interactive mode !!-->Method->"+method_name
									
									func(final_args,True)
								else:
									print "Launching without interactive mode !!--->"+method_name	
									func(final_args)
					
						self.IPexploit.UpdateStatus('complete',host,port,int(self.project_id),int(current_record_id))
					except Exception, ee:
							self.IPexploit.UpdateStatus('error-complete',host,port,int(self.project_id),int(current_record_id))
							print "EXception while executing exploits !: " +str(ee)
				
				
		
	def launchExploits(self):
		try:
			self.method_id="LaunchExploits()"
			self.print_Log("Started method LaunchExploits()")
			self.generate_report=True
			IPexploits_data=self.IPexploit.getIpExploits(self.project_id)
			print "here -->"
			if((IPexploits_data !=-1 ) and (IPexploits_data is not None )):
				
				
				print "--1---here -->"
			
				for exploit in IPexploits_data:
					current_record_id=exploit[0]
					service=str(exploit[4])
					host=exploit[2]
					port=exploit[3]
					self.print_Log("Service,Host,port  is -->"+str(service)+"  " +str(host)+"  "+str(port))
					entry=self.commandsJson.get(service)
					print "read"
					meta=entry.get('Commands') #check weather the obtained service is custom or not.If yes then the following code will throw exception and needs to be modified a little
					for entries in meta :
							method_name=entries.get('method')
							args=entries.get('args')
							self.commandObj.method_id=method_name
							self.commandObj.command_id=entries.get('id')
							self.commandObj.current_record_id=current_record_id
							self.commandObj.current_host=host
							self.commandObj.current_port=port
							self.commandObj.data_path=self.data_path
							final_args=[]
							for arg in args:
								if isinstance(arg, basestring):
									arg=arg.replace("<host>",host)
									arg=arg.replace("<port>",port)
								final_args.append(arg)
							if ((method_name)):
								func = getattr(self.commandObj,method_name)
								print "Invoking !!!"
								is_interactive=entries.get('interactive')
								self.commandObj.print_Log_info("\n\n\n STARTING EXPLOITS  FOR PROJECT ID --> " +str(self.project_id))
								print "Logged"
								if((is_interactive !=None ) and (is_interactive =="1")):
									print "Launching General interactive mode !!-->Method->"+method_name
									
									func(final_args,True)
								else:
									print "Launching without interactive mode !!--->"+method_name	
									func(final_args)
				
				


			
				
		except Exception ,ee:
			self.print_Error("Inside exception of launch exoloits :"+str(ee))

	def integration_test(self):
		print "Started\n"
		with open("all_commands.json","rb") as f:
	    		jsonpredatas = json.loads(f.read()) 
		#ftp=jsonpredatas.get('netbios-ssn')
		#ftp=jsonpredatas.get('ftp_command')
		#ftp=jsonpredatas.get('ssh')
		#ftp=jsonpredatas.get('smtp_command')
		#ftp=jsonpredatas.get('smtps_command')
		#ftp=jsonpredatas.get('pop3')
		ftp=jsonpredatas.get('imaps')
		#ftp=jsonpredatas.get('domain')
		#ftp=jsonpredatas.get('ldaps')
		#ftp=jsonpredatas.get('isakmp')
		#ftp=jsonpredatas.get('exec')
		#ftp=jsonpredatas.get('openvpn')
		#ftp=jsonpredatas.get('vnc')
		#ftp=jsonpredatas.get('finger')
		#ftp=jsonpredatas.get('ntp')
		#ftp=jsonpredatas.get('ms-sql-m')
		#ftp=jsonpredatas.get('nfs')
		#ftp=jsonpredatas.get('login')
		#ftp=jsonpredatas.get('snmp')
		#ftp=jsonpredatas.get('ms-wbt-server')
		#ftp=jsonpredatas.get('rsftp')
		#ftp=jsonpredatas.get('dhcps')
		#ftp=jsonpredatas.get('tftp')
		#ftp=jsonpredatas.get('rpcbind')
		#ftp=jsonpredatas.get('microsoft-ds')
		#ftp=jsonpredatas.get('shell')
		#ftp=jsonpredatas.get('oracle')
		#ftp=jsonpredatas.get('radius')
		#ftp=jsonpredatas.get('upnp')
		#ftp=jsonpredatas.get('squid-http')
		#ftp=jsonpredatas.get('mysql')
		#ftp=jsonpredatas.get('xmpp-client')
		#ftp=jsonpredatas.get('postgresql')
		#ftp=jsonpredatas.get('irc')
		ftp=jsonpredatas.get('http')
		print "read"
		meta=ftp.get('Commands')

		for entries in meta :
				method_name=entries.get('method')
				id_=entries.get('id')
				args=entries.get('args')
				host="192.168.179.136"
				port="80"
				final_args=[]
				if (id_=="http_2"):#replace it later by if 1:
					for arg in args:
						if isinstance(arg, basestring):
							arg=arg.replace("<host>",host)
							arg=arg.replace("<port>",port)
						final_args.append(arg)
					if ((method_name)):
						func = getattr(self.commandObj,method_name)
						print "Invoking !!!"
						is_interactive=entries.get('interactive')
						if((is_interactive !=None ) and (is_interactive =="1")):
							print "Launching mathod in General interactive mode !!"
							func(final_args,True)
						else:
							print "Launching mathod without interactive mode !!"		
							func(final_args)


#driverObj=Driver()
#driverObj.main()
#driverObj.integration_test()
#m.cleanUp()

	
"""for k,v in ftp.iteritems():
	#print "key :\n"+str(k) + "\nValue :\n" +str(v)
	for items in v :
		print str(values)+"\n\n"
		for 
		module_name=values.get('Script')
		method_name=values.get('method')
		if ((module_name ) and (method_name)):
			print "Module : "+module_name + "Method :" +method_name
for key_ in jsonpredatas.keys():
	for k in jsonpredatas.get(key_):
		print key_
		print k
#m = __import__ ('module_name')
#func = getattr(m,'method_name')
#func()"""


"""

{"Script":"commands","method":"meta_commands","args":["workspace -a ssh_version_tester\n","set THREADS 1\n","workspace ssh_version_tester\n","use auxiliary/scanner/ftp/anonymous\n","set RHOSTS 192.168.179.136\n"]}
"FTP_command":
			{
			"Metasploit_commands":[{"Script":"Metasploit.py","method":"meta_ftp","args":["workspace -a ssh_version_tester\n","set THREADS 10\n","workspace ssh_version_tester1\n","use auxiliary/scanner/ftp/ftp_login\n","set RHOSTS 192.168.179.136\n","set USERNAME root\n","set PASSWORD toor\n","set VERBOSE false\n"]}],"Terminal_commands":["val2"]
			}
"""
