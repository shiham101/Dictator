# What is PTO (Penetration Testing Orchestrator) ? :#
PTO  is a network penetration testing automation tool that automates port discovery and service scanning phases of penetration testing 

1.      Discovery (Port Scanning) -Nmap
2.  	Vulnerability Scanning (Service Scanning) -Metasploit ,Terminal automation ,nse ,open source (python ,ruby ,shell ,nse ,perl) scripts ,Kali Linux Built in tools.
3. 	PTO is developed in python and django and uses mysql at backend.
	
# Target Users #

1.   PTO will be useful for penetration testers as it automates most of the manual activities that penetration testers engage in  during testing. .

2.   On top of automation PTO improves performance of Penetration Testing by making use of thread parallelism for both port discovery and service scanning .

3. PTO is flexible and extendable : As of now PTO has automated 206 test cases of service scanning .The architecture adapted to design PTO is extendable i.e. without making change at code level ,we can add more external scripts /test cases /Metasploit models with PTO ,by just changing the settings file.

4. PTO comes in various modes of Operations for conducting Scan : 
    (a) Sequential Scan Mode
    (b) Concurrent Scan Mode
    (c) Sequential-Default Scan Mode.

# PTO Capabilities: #

	  Discovery Phase (Uses Nmap Internally) : 
		Discovery (Pause and Resume):Scan the entire port range of an entire subnet with the capability to pause and resume scan saving intermediate results. 
 		Discovery –Parallel Port Scanning :Port parallelism scanning breaks all ports into chunks and scans all chunks in parallel at one single  host and thus reduces scan time.
		Discovery –Thread Scheduling and Dispatching: PTO has a thread scheduling module, which ensures that maximum number of threads run  in parallel does not increase the chosen threshold and also schedules a new thread for a host any time it finds a host which is unscanned.
		Discovery and Report Upload: PTO has a result importer module, which can read the results from an existing Nmap.XML report file and can import the findings in our custom database, and further use these findings in order to launch service scanning. Thus this leaves user with the flexibility to use our tool in both modes (1) Discovery and exploits together (2)  Exploits mode alone 


	Reconfiguration Phase:
 		Reconfiguration of service helps to map services of type unknown to known types
		Reconfiguration helps to reduce false positives by manually validating the discovered service for its correctness using service version option.
		Add test case gives user the flexibility to reduce the false negatives by adding a host ,port service that Nmap might have missed but might be actually present.
		PTO has custom service classes like ssl that can be mapped with any given service such that additional ssl checks would be imposed apart from regular service checks.

	Service Scanning Phase:

		Scanning (Automation of  test cases) :
		PTO has automated 206 test cases which include Metasploit modules, Perl ,python ,java ,bash and ruby ,Nse  scripts, in a manner such that based upon the service detected, without any human intervention , the appropriate scripts would be launched
		and executed on the discovered host and port.

		Scanning (Terminal Automation and Metasploit Automation) :
		Apart from external scripts PTO has also automated the test cases which require multiple steps of human intervention as in Metasploit modules  that require multiple commands to be set ,tools like w3af_console[7] which need multiple configuration steps from user before launching an exploit or manual checks such as anonymous ftp login or logging in with default passwords ,which require a pen tester to open a terminal and type a series of commands to deduce to a conclusion towards vulnerability status of underlying service being tested. 

		Scanning (Packet Sniffing): 
		Some services require the underlying traffic to be sniffed in order to verify whether the sensitive data such as credentials or card details are 
		being passed in plain text or in encrypted way. PTO  also automates packet sniffing for the services where it is required and would generate 
		Pcap files for analysis by the penetration tester.

		Scanning (Threading) : 
		PTO provides the capability to launch scanning with threading enabled or without threading (default).
		The threading enabled invocation helps to run the test cases in a faster time.


	Reporting :
		HTML report and Console Decoding : Produces HTML output which looks very identical to output produced on console
		Report Merger : PTO has a report merger module which takes nessus xml report and qualys xml report as input and merges them with manual test cases in order to produce one final consolidated report which is available for download in 4 formats (HTML,json,XML,csv).
                CVE-Exploit Mapper : PTO has collected data from various sources and has a local repository that has mapping between CVE's and Exploits.Penetration Testers can use this capability to quickly map known CVE's to exploits.

# Architecture and Availability : #
*  The tool is available as a WEB service /API + web Application 
*  The WEB api is under the project dictator_service
*  The web application that consumes the web api is under the project dictator_client
 ![Image :](https://bitbucket.org/repo/5X5GyA/images/1154581580-arcitecture.png)

# KEY POINTS : #
* 	It must be noted that the web API does not have any authentication logic.
* 	All the user authentication is handled by the web application which consumes the services from web API 
* 	The web API only expects an application token which would authorize the application to access it.The application token can be found 
* 	in settings.py file of the client web application.
* 	It is recommended that the web API port should be blocked from external access or what would be even better would be to communicate from web application to
* 	web API through a UNIX socket
* 	Note that ,this tutorial will help you get started with using the tool PTO with django web /application server ,But django is a very light weight server which
* 	is not recommended for production environment.
* 	For commercial /production environment kindly use nginx + uwsgi or any other web + python application server of your choice.
* 	Following link helps you get started with nginx + uwsgi + django http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
* 	For this tutorial we are good to use django built in server.

# INSTALLATION STEPS : #
       Pull the code For PTO as follows :
             Pull/Clone code of dictator_service  : git clone <url>
             Pull /Clone code of dictator_client  : git clone <url>
             Downloading database nmapscan.sql     :The database is present at the root directory of Dictator Code base

# OTHER DEPENDENCIES : #

# Dependencies from Internet /Web: #

Either install them manually by typing each command in terminal

	apt-get install mdns-scan
	pip install python-nmap
	pip install python-libnmap
	pip install python-libnessus
	pip install lxml
	pip install django
	pip install djangorestframework
	pip install markdown       # Markdown support for the browsable API.
	pip install django-filter  # Filtering support
	sudo apt-get install python-mysqldb
	apt-get install python-magic
	pip install texttable
	pip install pyshark
	pip install ansi2html

Alternatively the above mentioned installables are also present in this shell script which can be run as :
	sudo sh install.sh



The following steps need to be performed maunally :


## Perl Dependencies  : ##

	Open cpan by typing following command :
	cpan

	Type following commands 
		install XML::Simple
		install Encoding::BER

## External Tool Dependencies : ##
	Installing Hoppy:
		Assuming you have downloaded dictator_service from git , go to the following path -
		cd dictator_service/Dictator_service/Scripts/hoppy-1.8.1/hoppy-1.8.1-
			Type-
				sudo make install

       Install Spvicious :
		 git clone https://github.com/EnableSecurity/sipvicious.git
		 cd sipvicious
		 python setup.py install



## Installing Mysql ##

	If you are using ubuntu 14.04,16.04,linux wheezy ,jheezy then follow the following :

		wget https://dev.mysql.com/get/mysql-apt-config_0.8.3-1_all.deb
		sudo dpkg -i mysql-apt-config_w.x.y-z_all.deb
		sudo apt-get update
		Link to refer :https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/#repo-qg-apt-upgrading

	If it is any other version of debian ,than the preferred way of installation is from the development packages 
		Tested on Kali-roling (5.7.15):

		Download the deb bundle DEB Bundle 5.7.*  https://dev.mysql.com/downloads/mysql/
		(mysql-server_5.7.17-1debian7_amd64.deb-bundle.tar)

		After download follow these steps :
			tar -xvf mysql-server_MVER-DVER_CPU.deb-bundle.tar
			sudo apt-get install libaio1
			sudo dpkg-preconfigure mysql-community-server_*.deb
			sudo dpkg -i mysql-{common,community-client,client,community-server,server}_*.deb
			sudo apt-get -f install

		Alternatively you may reffer to following URL :
			https://dev.mysql.com/doc/refman/5.7/en/linux-installation-debian.htm



## Getting STARTED : ##

First create following databases :
 mysql -u <user_name> -p <password>
	create database nmapscan;
	create dictator_client;
	exit;

Restoring the Web service /API databse :
	mysql -p  nmapscan < nmapscan.sql 


### Setting Database Password for Client /Web application <dictator_client>  : ###
	Go to the path where your dictator_client would be and make sure you have current db username and password in settings.py file 
	</dictator_client/Dictator_client/settings.py>

	Under the entry DATABASES { 

		'NAME': 'dictator_client',
        	'USER': 'sql user',
        	'PASSWORD': 'mysql password',
        
				}
## Setting Database Password for Dictator Service -Web Service : ##
	 Open the text file at the path : cd dictator_service/Dictator_service/db_file.txt
	 The text file would be having dummy <username:password> for your mysql database .
	 Update the username password from root:toor_pw to <your_username>:<your_password>

## Sync Web application Database tables : ##
	cd dictator_client 
	Then create database tables for client application by running following command :
	python manage.py makemigrations
	python manage.py migrate


## Running Dictator_client : ##

To get Started Create an admin /Superuser .This user will be Having Role admin at Django administration .
But with application ,it will be having role of normal user.
	
	python manage.py createsuperuser
	provide username ,password ,email etc.
	Finally run the web application by using the command 
	python manage.py runserver 8000
	Then browse to http://127.0.0.1:8000/admin 

	Add users to user table and and same user would be added to profile table where you can go and change the user role 
	By default the role would be "user" with normal privileges and other role would be "admin" with admin privileges.
	
	Admin user has more privileges and can view /pause /resume scans of all users.



## Running Dictator_service : ##

	To get started with Dictator service :

	Issue following command :python manage.py runserver 8002 #8002 as the web service /API consumer expects the service to be served on port 8002


# Understanding Master JSON - #

•	The purpose of this section is to guide a penetration tester about how he can Update the master JSON file if required.

•	The utility of Master json file is to map Services with the test cases. This file will actually contain the key value pairs ,where the key is the Service and the values are the set of test_cases which are meant to be executed against that service.

•	Path : /root/Django-projects/Dictator/Dictator_service/Scripts


•	Actual Architecture :

o	The structure followed by master json file is : 

Key<service name>: value (A dictionary having a list of dictionaries) –Example
![Master_json.png](https://bitbucket.org/repo/7576gx/images/470669311-Master_json.png)


o	Method ID: The Method ID signifies the various methods which have been developed and placed in the auto_commands.py module which would be responsible for executing various test cases. 

o	Command ID: The Command ID is unique identifier for each command. It would help in storage and retrieval of Test case results. 

o	Custom: The Custom flag suggests whether it’s a known service json class or a customized service json class. What we mean by a customized service json class is that, suppose there is a service class which is defined for a service like ‘http’, the class has all the checks which are meant to be performed for ‘http’ but for a service like ‘https’. Ideally, the checks will include all the http checks and all the ssl checks. Thus, it is ideal not to repeat the checks by typing them manually over and over again. Instead we can make a class named ‘ssl’ and for ‘https’, inside the commands key, the value can be ‘http’, ’ssl’ and the custom flag set to ‘true’. This would perform all the checks for http as well as ssl on the given service: ‘https’

o	Methods: The methods are nothing but Python functions that cater different attack/service scanning vectors. They are broadly classified into the following categories :
 
	Single Line methods <with time out>,

	 Metasploit methods,

	Single line methods <without timeout>

	 General interactive,

	Traffic Sniffing methods,

	Other miscellaneous methods.

Although the general template structure would remain to be same for all the methods mentioned, but the augments passed on to the methods would vary depending upon category of methods

# 1.	Metasploit Test Cases # 

![Master_json_metasploit.png](https://bitbucket.org/repo/7576gx/images/2666964196-Master_json_metasploit.png)

	"ftp" - It specifies the service for which the test cases are to be configured.

	The value of this key "ftp" ,is a dictionary and that dictionary has following entries 
:
•	Commands : This is a very crucial entry and it holds a list of dictionaries. Each dictionary actually holds a test case. The structure /entries of each dictionary inside commands is :  Dict { }  

o	args[] -Args is a list and would hold the arguments which are required to execute the external script. In actuality it will hold the commands meant to be executed to perform service scanning. In the current example it will hold the ,set of commands required to execute the Metasploit module .Notice that the values of host and port are specified in angular brackets ,as they are expected to be read from discovery phase /port scanning .At runtime the values are read and <host> <port> are replaced with appropriate values of target  to be scanned. Thus for Metasploit test cases the args will hold the list of commands expected by the Metasploit module and the essential parameters expected by Metasploit module.

o	ID :Unique id given to test case

o	method :The actual method /python code that will get executed. All the MetaSploit test_cases are handled by the method "custom_meta"

o	Title :It could be any title that u may wish to name your test case with
Thus likewise there would be many such dictionaries inside commands [] list and each will point towards a test case .

•	Custom :This flag takes a value True /False .If it's True ,it means that the service class is a custom service class like https [http + ssl] , ftps [ftp + ssl] and etc.

# 2.	Single Line commands and Sniffing Test cases : #

The single line test_cases are the ones which require only one line command to invoke the test case and would not require further interaction with test case script /For example nse scripts ,python scripts ,Perl scripts ,java class modules ,etc which can be invoked as one liners and they would get executed and finally would provide us with output.

![Master_json_single_line.png](https://bitbucket.org/repo/7576gx/images/3591983543-Master_json_single_line.png)

![Master_json_single_line_ex_sc.png](https://bitbucket.org/repo/7576gx/images/3621354201-Master_json_single_line_ex_sc.png)

•	Commands : The structure /entries of each dictionary inside commands is :  Dict { }  

o	args[] -Args is a list and would hold the arguments which are required to execute the external script. . In the current example it will hold the timeout value as first argument and as second argument it will hold the  command that we wish to execute on the operating system which would invoke the external script   . You can see in this case there are values of nse scripts ,nikto ,hoppy  that we wish to execute on terminal against the target host /port and for each  script we are passing a timeout value as first argument.

o	ID :Unique id given to test case

o	method :The actual method /python code that will get executed. All the Single line test cases  are handled by the method "singlelineCommands_Timeout" and all the test cases which would require to sniff traffic in background will be handled by method general_commands_Tout_sniff .

o	Title :It could be any title that u may wish to name your test case with

# 3.	General Interactive and Sniffing Test cases : #

With our automation scripts we not only cover the use cases that would invoke an external script (Python, Ruby, shell, etc.) and collect the findings, but we have also been able to  automate the use cases which require multiple steps of human intervention. Tools like “w3af_console” that need multiple steps of terminal interaction from user before actually performing the scan or manual checks such as anonymous ftp ,telnet anonymous  login or logging in with default passwords. This requires a pen tester to open a terminal and type a series of commands to deduce to a conclusion towards vulnerability status of underlying service being tested. We have been able to achieve this capability using virtual consoles. 

![general_interactive.png](https://bitbucket.org/repo/7576gx/images/2983942768-general_interactive.png)


•	Commands : The structure /entries of each dictionary inside commands is :  Dict { } 
 
o	args[] -. In the current example "General_interactive_test_cases"

o	The template structure of args [] can be given as [ Timeout , Command , [List], Print_Command ,[List] ,Print_Command ... ]

	Timeout-It will hold the timeout value as first argument

	 Command -Second argument it will hold the  command that we wish to execute on the operating system which would invoke the external script /service  .

	[List] - The 3rd ,5th ,7th and so on (odd number indexes after 1) ,will hold a list .This list will have following arguments :

•	The first argument will hold the index of the element ,that would indicate a expected response produced by the terminal and would indicate the code to keep progressing. 

•	The remaining arguments will hold the regular expression patterns of all the possible outputs that the terminal window /external script / external service can produce and amongst them one of the output will represent expected output which would be specified by the first argument 

•	Example :In the given scenario ,in the list which is at index 2 of args [ ]  (after command ftp <host> <port>) ,it can be seen that "2" is the first element of the list. It means the element at index 2 of this list will represent an expected output from target. At index 2 we have  "Name .*" .It means that ideally if we do ftp <host> <port> and ftp service would be running ,the target usually responds back asking for Name of the user who wishes to login. Thus "Name .*" ,here represents the response in ideal case. Note .* is a regular expression closure symbol which means anything can appear after Name ,finally there must be a colon like ":".

•	Print_Command  -Thus if remote target asks for Name ,the third argument  will be the output we wish to pass on the virtual terminal or to the target ,in this case it is "anonymous" ,as we are checking for anonymous login.

•	Again now we pass a list which will have success response index at first index /item ,and will contain list of other expected outputs produced by the remote service /target. Note amongst these outputs one might be the successful output. In this case if everything goes well ,we would expect the service to ask us for password ,that's why we are passing index of 0 ,at which we have regular expression string ".* Password :" ,which means anything before (which could be host name ) ,and finally Password of host.

•	Finally we go ahead and supply password as dummy_password@anonymous.com 

•	If the remote service would allow anonymous login then we may expect a console like ftp > ,thus we pass it in next list with index 0 as success index.

•	It must be noted that ,if there are multiple indexes that may represent successful response ,then we can specify them in comma separated manner like 1,2,3

o	ID :Unique id given to test case

o	method :The actual method /python code that will get executed. All the General interactive test cases   are handled by the method "general_interactive" and all the test cases which require sniffing as well while executing of test case ,will be handled by "general_commands_Tout_sniff" and if they would be interactive the interactive flag will be set=1

o	Title :It could be any title that u may wish to name your test case with

o	interactive :It specifies whether the test case is interactive or not. For all interactive the value would be =1.



# 	To Update Master JSON (Summary) # :

o	In order to update master JSON  ,if we wish to add a test case to Master JSON ,we need to identify which category the test case would belong to :

	Single line commands.

	General Interactive.

	Metasploit module.

	Single line with sniffing.

	General interactive with sniffing.

o	Based upon the category of script / service /test case we wish to automate ,we add it to appropriate service key ,and invoke appropriate method ,passing on valid arguments.

## 	Valid Arguments Single line commands   ## :

•	args [ ] -
o	First argument =Timeout
o	Second argument is command to be executed
•	Method -singlelineCommands_Timeout

## 	Valid Arguments Metasploit    ## :

•	args [ ] -List of commands expected by the MetaSploit auxiliary /scanner module
•	Method -Custom_meta

## 	Valid Arguments General Interactive and General interactive with sniffing. ## :

•	args [ ] 

o	First argument =Timeout

o	Second argument = External Command  

o	 [List] - The 3rd ,5th ,7th and so on (odd number indexes after 1) ,will hold a list .This list as first item will hold the index of element that may represent expected output produced from target (match string to proceed),and the remaining elements will hold the list of all expected outputs that target may produce ,one or multiple of which may represent successful / expected output.

o	Print_Command :The 4th ,6th ,8th (even number indexes after 2) ,will actually hold the command /text which a test case is supposed to print on the terminal assuming the last produced output was as expected.

•	Method :

o	general_interactive (without sniffing ) , 

o	general_commands_Tout_sniff (with sniffing)

•	Interactive : Set this flag =1 for all interactive test cases

## 	Valid Arguments :Single line with sniffing  ## :

•	args [ ] -

o	First argument =Timeout

o	Second argument is command to be executed

•	Method - general_commands_Tout_sniff

•	Interactive : Set this flag =0 for Single line with sniffing.


# 5.	Usage [PTO -GUI]  # :

## •	Scanning Modules  ## :

•	Based upon the type and nature of scans being conducted on underlying infrastructure, the pen tester has got multiple options available and may choose the one that may fit in best with the given infrastructure to be tested. The various modes of usage available are:

### o	Sequential Mode ### :
 In sequential mode, the tool would start with the discovery followed by reconfiguration and then it will start service scanning. Thus, it is a three step process. Note that in sequential mode :

![sequential.jpg](https://bitbucket.org/repo/7576gx/images/2446128188-sequential.jpg)

•	The service scanning cannot be started till all hosts haven't been scanned

•	Once service scanning is started no reconfiguration could be done .

•	Service scanning once started ,would be started for all services .User has no control over what services to scan first and what to scan at last.

### •	Reconfiguration after Discovery Would be over  ### :

In order to reduce false positives and false negatives ,kindly analyze port scanning results and if required ,reconfigure / change them and you may additionally add test cases if in case any service / port is left out. 

![reconfig_1.jpg](https://bitbucket.org/repo/7576gx/images/530319620-reconfig_1.jpg)

![reconfig_2.jpg](https://bitbucket.org/repo/7576gx/images/1033413368-reconfig_2.jpg)


•	In the above figure we are changing service of type "status" to type "ftp" .Thus the test cases would be run for ftp.Note :Do that only when you are sure that the service discovered is incorrect or of type "Unknown" .We shall understand service types shortly.

•	Add test case :If nmap may miss out host /port /service ,add that manually as follows :

![add_test_case.jpg](https://bitbucket.org/repo/7576gx/images/378465611-add_test_case.jpg)

•	After adding test case we can click upon start scanning option to begin with service scanning. We can choose to enable threading option in order to speed up the results ,and we can also go and start service scanning without threading option. As shown below:

![added_test_case.jpg](https://bitbucket.org/repo/7576gx/images/809506929-added_test_case.jpg)


•	Viewing intermediate results :The moment a person clicks upon Start scanning ,he / she would be redirected to scanning page. Every time a test case would be executed the UI would be updated and a blue color icon would appear on the screen in front of the service being scanned. A user may click upon that icon and can view the test case results.

o	Note : When all the test_cases for a service would be executed then the icon will turn green.

•	Following diagram shows intermediate test case results :

![view_test_case_res.jpg](https://bitbucket.org/repo/7576gx/images/4057313099-view_test_case_res.jpg)

•	At any point a user can leave the UI ,the running scan will not get impacted. Suppose the user may wish to see currently running scans .From the scan tab at top ,he may choose running scans .The following screen would be displayed :

![All_Scans.jpg](https://bitbucket.org/repo/7576gx/images/2751621350-All_Scans.jpg)


•	Depending upon the state of the scan the action column ,will display appropriate action. If the scan would be under progress the action column will have action as  "Ongoing". A user may click upon this button and will get to the UI screen of the current state of his / her scan.

•	A user can click upon the name of the scan ,in order to see the configuration (hosts ,ports ,switch ) with which the scan was initially launched.

### o	Concurrent Mode ### :

	In Sequential mode, the service scanning can't be started till port scanning results would be available for all the ports and hosts being scanned. Thus, a pen tester may have to wait to obtain results and also in this mode, the pen tester does not have control over which services he would want to scan first and which later. All the services are scanned in one go, limiting granularity of control over service scanning. These are the limitations of the sequential mode that are handled by the concurrent mode.

	The Concurrent mode offers the flexibility to launch service scanning the moment service discovery would be finished and further gives an option to launch service scanning for selective services based upon pen testers choice.

	Click Upon New scan tab Under the scan tab option .

	Fill in the scan parameters and choose the scan mode as Concurrent.


![concurrent.jpg](https://bitbucket.org/repo/7576gx/images/979384770-concurrent.jpg)

	The remaining steps will be same ,just that in this mode of scan ,a user will not have to wait for all hosts and ports to be scanned, to begin with service scanning ,also the user can choose what services he may wish to scan :Following figure displays same :

![results_conc.jpg](https://bitbucket.org/repo/7576gx/images/4286344808-results_conc.jpg)

	As you can see in above screen shot ,user choose to scan http first and does not scan Ssh immediately ,Its at users will when he would want to scan what service.

	All the capabilities (reconfiguration ,viewing results and etc ) are available with concurrent mode also.


### •	Sequential Default Mode ### :
With this mode the service scanning would start immediately after discovery would be over, skipping the reconfiguration phase. The utility of this mode is more relevant in case of scheduling scans where the pen tester may schedule scans to start at some time and may not be available to do the reconfiguration and may want to proceed with default port scanning results for service scanning . Thus this mode of scan skips the reconfiguration phase and directly launches service scanning on default nmap port scanning results.

	Click Upon New scan tab Under the scan tab option .

	Fill in the scan parameters and choose the scan mode as Sequential Default.

![seq_def.jpg](https://bitbucket.org/repo/7576gx/images/678003689-seq_def.jpg)

	When port scanning results would be over it will start service scanning ,by itself ,irrespective of  whether the user is currently logged in or not.


# •	Pausing and Resuming Scans  # :

o	Irrespective of the mode of scan ,any scan weather in discovery or service scanning state ,can be paused. The intermediate results would be saved and the user can resume the scan anytime in the future.

o	It must be noted that ,if the scan is paused while discovery (port scanning would have been going on ) ,then the port scanning results for the ports that must have been scanned  would be saved and when user resumes ,the scan would start for un scanned ports .Likewise if the scan is paused during service scanning ,then whatever services would have been scanned ,there results would be saved and the user gets the flexibility to analyze the results of the services that would be scanned. When the scan would be resumed ,the service scanning will start for unscanned services.

o	Following screen shots show how to pause an ongoing scan .


![ongoing_scan.jpg](https://bitbucket.org/repo/7576gx/images/591328815-ongoing_scan.jpg)

o	In order to resume the scan ,either go to the current scans tab or go to the paused scans tab. The action column by default would be having two buttons :

	Resume :This will resume the scan from whatever state it would have been paused and would go ahead and continue scanning.

	Analyze :If the scan would be paused while service scanning ,then if the penetration tester may wish to analyze the results for the services that were already scanned ,but would not wish to resume the scan ,then he / she may choose the option analyze. With this the user can get to see intermediate test case results for completed services.

	Note : Analyze option may not appear if the scan would be paused during port scanning ,as there would be no test_cases executed to analyze if port scanning would be going and mode would not be concurrent .

	Note : Analyze option does not appear for concurrent scans ,the resume button will perform that joint functionality of resuming and analyzing the scans invoked in concurrent mode.

![resume_analyze.jpg](https://bitbucket.org/repo/7576gx/images/3272206393-resume_analyze.jpg)


## •	Downloading Reports  or Analyzing when Scan would be completed  ## :

o	When the scan would be finished ,the user will get the option Download all ,on the UI .If the user would visit the current scans tab ,for all the scans with status as complete for both discovery and service scanning ,the action column ,will by default have an option to download the  results for offline analysis or to analyze the results online itself.

![download_analyze.jpg](https://bitbucket.org/repo/7576gx/images/22949813-download_analyze.jpg)

o	On  clicking Download all ,a zipped folder would be downloaded. It will have :

	The final HTML report containing all test case results.

	It will have all Pcap files which would sniff certain services where sniffing is required. The Pcap files can be opened with Wireshark and analyzed weather the text / credentials are passed as plain text or in encrypted format. Note :The name of the Pcap file would be like  <project_id>_<host>_<port>_capture_output.pcap.Thus if sniffing is done on host1 for port 21 and project id 100 ,the Pcap file name would be 100_host1_21_capture_output.pcap.

	The downloaded folder will also have the final chosen configuration (Services -Test cases) with which the scan was launched .(JSON format)

o	On the other hand clicking upon Analyze tests will take us to UI where we can see the results of all test_cases on the user interface only.


# •	Reporting # :

o	 Nmap Report Upload - To use it ,go to Upload Reports and choose Nmap report . 
Its a result importer module, which can read the results from an existing Nmap.xml report file and can import the findings in our custom database, and further use these findings in order to launch test cases/service scan. Thus, this leaves the user with the flexibility to use our tool in both modes (1) Discovery and service scanning together (2) Service scanning mode alone

![report_dash_board.jpg](https://bitbucket.org/repo/7576gx/images/2083522804-report_dash_board.jpg)


![nmap_xml.jpg](https://bitbucket.org/repo/7576gx/images/3362623830-nmap_xml.jpg)

	On clicking upon upload the report will be parsed and uploaded ,a user may go to current scans and would find the uploaded project "test_upload_nmap" listed over there ,with its discovery status and complete and service scanning status as incomplete. A user may click upon action tab "ongoing:" and can reconfigure the results and then start service scanning.



Qualys and Nessus Report Parsers-

	To use this option Go to Upload reports tab and select either Qualys/Nessus Report. 
We  have a report merging module, which would merge the results obtained from Qualys, Nessus and manual test cases. In order to merge the reports, they have to be parsed first .We have Qualys, Nmap and Nessus report parsers. All of them will take a report in XML format and would parse the report and place it in local storage so that querying and integrating the results with other reports becomes easier.

![qualys_nessus.jpg](https://bitbucket.org/repo/7576gx/images/3174782953-qualys_nessus.jpg)

	Note that the purpose of uploading the report here is to merge it with some manual project. Thus select the project from drop down list with which a user may wish to merge the nessus /Qualys report.


o	Report Merger : 

	To use this option Go to Merge reports tab and select the ID/Name of the manual project with which you wish to integrate the qualys and nessus Results. 

	It assumes that the nessus and qualys reports would have already been uploaded and linked to the project with which they are meant to be merged .

	This module merges the manual test cases, parsed Qualys report, parsed Nessus report and would also map the CVEs to exploits and finally, would provide the user an option to download the integrated reports in any of the format amongst (XML, HTML, CSV, JSON) thus providing one consolidated view for analysis.

![merger_home.jpg](https://bitbucket.org/repo/7576gx/images/720317329-merger_home.jpg)

![merger.jpg](https://bitbucket.org/repo/7576gx/images/1868737616-merger.jpg)

	The final downloadable report is available in four formats (HTML, CSV ,JSON ,XML).

	Note :The merged report will do the merging based upon common <host><Ports> found in nessus /qualys and manual test_cases. It will cluster common host , port into one group ,such that analysis becomes easier.
