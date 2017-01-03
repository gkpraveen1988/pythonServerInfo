import os,sys,argparse
myList = ''
# Function for passing the correct option and get the option values
def getArgs():
   parser = argparse.ArgumentParser(
         description='Script for taking the required data and pushing the influxdb')
   parser.add_argument(
         '-s', '--server', type=str, help='End server', required=True)
   args = parser.parse_args()
   return args

def printServerInfo(hostname):
   global myList
   cmd = 'a4 ssh -q '+hostname+' "sudo ifconfig" | awk \'{print $1}\' | awk \'/.*:/ { print }\' | sed s/://g| sed /^$/d'
   noOfDisks=os.popen(cmd).read().strip()
   diskOutput = noOfDisks.split('\n')
   print "Disks Attached to the Server "+hostname
   print "---------------------------------------"
   for disk in diskOutput:
      if disk != 'lo':
         cmd2 = 'a4 ssh -q '+hostname+' "sudo ifconfig '+disk+'"| grep ether| awk \'{print $2}\''
         macadd = os.popen(cmd2).read()
         output=disk+' = '+macadd
         myList+=output
   print myList

   cmd3 = 'a4 ssh -q '+hostname+' "sudo dnsdomainname"'
   domainZone=os.popen(cmd3).read().strip()
   print "DomainZone\n-------------\n"+domainZone+"\n"

   cmd4 = 'a4 ssh -q atest301 "sudo parted -l | grep \'^Disk /dev\'" | awk \'{print $2}\' | sed s/://g'
   diskAvailable=os.popen(cmd4).read().strip()
   print 'DiskInfo\n------------\n',diskAvailable

cmdLineArgs = getArgs()
printServerInfo(cmdLineArgs.server)
