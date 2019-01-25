import xmlrpclib
import os

class RemoteGuiManager:
	
	def __init__(self):
		
		pass
		
	#def init
	
	def get_first_display_free(self):
		'''
		Returns firs Display free from 42
		'''
		
		try:
			display=42
			while(os.path.isfile('/tmp/.X'+str(display)+'-lock')):
				
				'''
				# There is lock file... is it in use?
				print ("File "+'/tmp/.X'+str(display)+'-lock'+" exists")
				f = open('/tmp/.X'+str(display)+'-lock', 'r')
				for line in f:
					if (os.path.exists("/proc/"+line.strip())):
						print ("Any process is running on :"+str(display))
						# check another display
						display=display+1
					else:
						print("No process locking file, remove lock file")
						os.remove('/tmp/.X'+str(display)+'-lock')
						# Return removed display
						return ":"+str(display)
				'''
				
				display+=1
				
			return ":"+str(display)
		except Exception as e:
			print "Captured: "+str(e)
			return {'status': False, 'msg':'[RemoteGuiManager] '+str(e)}
		return ":42"
		
	#def get_first_display
	
	def remote_execute(self,local_user,cmd,remote_ip,remote_user,remote_password,force_root=False,xephyr_options=""):

		try:
			
			display=self.get_first_display_free()
			xephyr="Xephyr -ac " + xephyr_options + " " + display
			objects["GuiLauncherManager"].execute("",local_user,xephyr)
		
			remote_info=(remote_user,remote_password)
			client=xmlrpclib.ServerProxy("https://"+remote_ip+":9779")
			return client.execute(remote_info,"GuiLauncherManager","",remote_user,cmd,display,force_root,True)
		
		except Exception as e:
			print e
			return -1
		
		return 0
		
	#def remote_execute
	
	
#class RemoteGuiManager
