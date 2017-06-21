import json,time
import multiprocessing
import os
import threading

def test_threads():
	start_time=time.time()
	thread_pool=[]
	for i in range(1,10):
		t=threading.Thread(target=test_thread,args=(i,))
		thread_pool.append(t)
		t.start()
	for th in thread_pool:
		th.join()
	end_time=time.time()
	total_time=end_time-start_time
	print "Total time taken with threading : " +str(total_time)

def test_thread(thread_id):
	
	for i in range(1,5):
		with open(os.path.join("/root/Desktop/junk/","Thread_"+str(thread_id)+"_File_"+str(i)+".txt"),"w+") as out:
			for j in range(1,1000000):
				out.write("Line "+str(j))
				out.write("\n")


def test_processes():
	start_time=time.time()
	process_pool=[]
	for i in range(1,10):
		t=multiprocessing.Process(target=test_process,args=(i,))
		process_pool.append(t)
		t.start()
	for pr in process_pool:
		pr.join()
	end_time=time.time()
	total_time=end_time-start_time
	print "Total time taken with processing : " +str(total_time)

def test_process(process_id):
	
	for i in range(1,5):
		with open(os.path.join("/root/Desktop/junk/","Process_"+str(process_id)+"_File_"+str(i)+".txt"),"w+") as out:
			for j in range(1,1000000):
				out.write("Line "+str(j))
				out.write("\n")
	print "Process : "+str(process_id) +"Ended \n"

def test_hybrid_threads():
	start_time=time.time()
	thread_pool=[]
	for i in range(1,10):
		t=threading.Thread(target=test_hybrid_process,args=(i,))
		thread_pool.append(t)
		t.start()
	for th in thread_pool:
		th.join()
	end_time=time.time()
	total_time=end_time-start_time
	print "Total time taken with HYbrid model : " +str(total_time)

def test_hybrid_process(id_):
		#for i in range(1,10):
		t=multiprocessing.Process(target=test_process_hybrid,args=(id_,))
		#process_pool.append(t)
		t.start()
		t.join()
	
def test_process_hybrid(process_id):
	
	for i in range(1,5):
		with open(os.path.join("/root/Desktop/junk/","HYbrid_Process_"+str(process_id)+"_File_"+str(i)+".txt"),"w+") as out:
			for j in range(1,1000000):
				out.write("Line "+str(j))
				out.write("\n")
	print "Hybrid Process : "+str(process_id) +"Ended \n"


#test_threads()
#test_processes()
test_hybrid_threads()


