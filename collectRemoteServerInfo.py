# Purpose: Python scripts to fetch the remote server information (Domain name, Mac address of the nic cards, Number of disks)

import os,sys,argparse
macList = ''
# Function for passing the correct option and get the option values
def getArgs():
   parser = argparse.ArgumentParser(
         description='Script for taking the required data and pushing the influxdb')
   parser.add_argument(
         '-s', '--server', type=str, help='End server', required=True)
   args = parser.parse_args()
   return args

def displayServerInfo(hostname):
   global macList
   # Fetching the mac address for the nic card attached
   diskCmd = 'a4 ssh -q '+hostname+' "sudo ifconfig" | awk \'{print $1}\' | awk \'/.*:/ { print }\' | sed s/://g| sed /^$/d'
   nicCardAttached=os.popen(diskCmd).read().strip()
   splitNicInfo = nicCardAttached.split('\n')
   print "Mac Address for the NIC cards of server: "+hostname
   print "---------------------------------------"
   for ethernetAdapter in splitNicInfo:
      if ethernetAdapter != 'lo':
         fetchMac = 'a4 ssh -q '+hostname+' "sudo ifconfig '+ethernetAdapter+'"| grep ether| awk \'{print $2}\''
         macadd = os.popen(fetchMac).read()
         finalOut=ethernetAdapter+' = '+macadd
         macList+=finalOut
   print macList

   # Collecting the domain name information
   domainName = 'a4 ssh -q '+hostname+' "sudo dnsdomainname"'
   domainZone=os.popen(domainName).read().strip()
   print "DomainZone\n-------------\n"+domainZone+"\n"

   # Collecting the disk information
   noOfDisks = 'a4 ssh -q atest301 "sudo parted -l | grep \'^Disk /dev\'" | awk \'{print $2}\' | sed s/://g'
   diskAvailable=os.popen(noOfDisks).read().strip()
   print 'DiskInfo\n------------\n',diskAvailable

cmdLineArgs = getArgs()
displayServerInfo(cmdLineArgs.server)
