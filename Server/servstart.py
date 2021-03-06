import settings, sink, sys, time, thread, threading, utils

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage : python <script_name> <IP-address>")
		#<Controller-IP> <Control-Port> <Command-port> <Data-Port> <Size_of_Ring_Buffer> <Predictions> <No_of_Connections> 
		sys.exit()

	do_exit = False
	
	#intitialize port, number of clients, buffer size, etc
	servconfig = sink.Config()

	#Command-port starts listening for any commands from controller in future
	#Spawns thread internally when constructor is called
	Scanner = utils.Scan(servconfig)

	#Send JOIN! request to controller
	status = utils.Control._join(servconfig)

	#if controller declines JOIN request
	if(status!=0):
		do_exit = True
		print("JOIN request declined, cannot proceed")
		Scanner.stop()
		servconfig.command.close()
		servconfig.receiver.close()
		sys.exit()

	get = sink.ReceiveFrames()
	put = sink.AlprProcessing()
	
	thread2 = threading.Thread(name="Get_Frames", target= get._get_stream, args=(servconfig,))
	thread3 = threading.Thread(name="Process_Frames", target= put._put_alpr, args=(servconfig,))
	thread2.start()
	print("started get frames thread")
	thread3.start()
	print("started put frames thread")

	
	while do_exit==False:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt:
			do_exit = True

	Scanner.stop()
	servconfig.command.close()
	servconfig.receiver.close()
