import os
import subprocess
import threading
import xmlrpclib
import pwd


class GuiLauncherManager:
	
	def __init__(self):
		
		self.display={}
		
	#def init


	def register_display(self,user,display):
		
		display=display.split(":")
		if len(display)>1:
			display=":"+display[1]
		else:
			display=":"+display[0]
		
		self.display[user]=display
		
		return True
		
	#def register_display


	def get_display(self,user,ip):
		
		p=subprocess.Popen(["who"],stdout=subprocess.PIPE)
		output=p.communicate()[0].split("\n")
		displays=[]
		gtty_found=False
		for line in output:

			if user in line:
				if "tty" in line:
					tmp=line.split("tty")[1][:1]
					tmp=int(tmp)
					if tmp>=7:
						gtty_found=True
				line=line.split(" ")[-1]
				if "(" in line and ")" in line and ":" in line:
					displays.append(line[1:len(line)-1])
		
		for display in displays:
			if ip in display:
				return display
		
		if len(displays)>0:
			return displays[0]
		
		if len(displays)==0 and gtty_found:
			return ":0"
		
		if user in self.display:
			return self.display[user]
		
		return None
	
	#def get_display
	

	
	def execute(self,ip,user,cmd,force_display="",force_root=False,use_ip=False):
		
		
		try:
			xauth_file=pwd.getpwnam(user).pw_dir+"/.Xauthority"
			if force_display=="":
			
				try:
					display=self.get_display(user,ip)
				except Exception as e:
					
					raise e
				if display==None:

					return -1
					
			else:
				display=force_display
			
			if use_ip:
				display=ip+force_display
				
			if force_root:
				
				user="root"
			
			cmd="XAUTHORITY=%s DISPLAY='%s' su -c '%s' %s "%(xauth_file,display,cmd,user)
							
			print("[GuiLauncherManager] Executing %s ..."%cmd)
			t=threading.Thread(target=self._exec,args=(cmd,))
			t.daemon=True
			t.start()
			
			return 0
			
		except Exception as e:
			print e
			return -1
		
	#def callback
	


	def _exec(self,cmd):
		
		os.system(cmd)
	
	#def _exec
	

	
#class GuiLauncherManager

if __name__=="__main__":
	
	i=GuiLauncherManager()
	
	print i.get_display("cless","")