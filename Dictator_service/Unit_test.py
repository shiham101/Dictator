import sys
import auto_commands_ as auto_commands
import json
def Usage():
	print "python Unit_test.py <host> <port> <service_name> <test_case_id>"
	#print "The test case id is optional"
def integration_test():
	try:
		commandObj=auto_commands.Commands()
		with open("all_commands.json","rb") as f:
	    		jsonpredatas = json.loads(f.read()) 
		
		if len(sys.argv) < 5:
			Usage();
			return

		service=jsonpredatas.get(sys.argv[3])
		meta=service.get('Commands')
		test_case=None
		if len(sys.argv) ==5:
			test_case=sys.argv[4]

		for entries in meta :
				method_name=entries.get('method')
				id_=entries.get('id')
				args=entries.get('args')
				host=sys.argv[1]
				port=sys.argv[2]
				#print test_case
				final_args=[]
				if (test_case !=None):
					if (id_== test_case):#replace it later by if 1:
						for arg in args:
							if isinstance(arg, basestring):
								arg=arg.replace("<host>",host)
								arg=arg.replace("<port>",port)
							final_args.append(arg)
						if ((method_name)):
							func = getattr(commandObj,method_name)
							print "Invoking !!!"
							is_interactive=entries.get('interactive')
							if((is_interactive !=None ) and (is_interactive =="1")):
								print "Launching mathod in General interactive mode !!"
								func(final_args,True)
							else:
								print "Launching mathod without interactive mode !!"		
								grep= entries.get("grep",None)
								if grep != None:
									grep_commands=entries.get("grep_commands")
									func(final_args,grep_commands)
								else:
									func(final_args)
	except Exception ,ex:
			print "Exception occured : "+str(ex)
integration_test()
