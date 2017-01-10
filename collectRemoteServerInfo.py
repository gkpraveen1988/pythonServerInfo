# Purpose: Python scripts to fetch the remote server information (Domain name, Mac address of the nic cards, Number of disks)

import os,sys,argparse,pdb
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
   diskCmd = 'a4 ssh -q '+hostname+' cat /proc/net/bonding/bond0 | grep -A 7 \"^Slave Interface\"| grep  \"^Slave\ Inter\|MII\|Permanent\"| awk \'{print $NF}\'| sed \'N;N;s/\\n/ /g\''
   nicCardAttached=os.popen(diskCmd).read()
   splitNicInfo = nicCardAttached.strip('\n').split('\n')
   print "Mac Address for the NIC cards of server: "+hostname
   print "---------------------------------------"
   for nicInfo in splitNicInfo:
      nicInfo = nicInfo.split(' ')
      if nicInfo[1] == 'up':
         print nicInfo[2]

   # Collecting the domain name information
   domainName = 'a4 ssh -q '+hostname+' "sudo dnsdomainname"'
   domainZone=os.popen(domainName).read().strip()
   print "\nDomainZone\n-------------\n"+domainZone+"\n"

   # Collecting the disk information
   noOfDisks = 'a4 ssh -q atest301 "sudo parted -l | grep \'^Disk /dev/sd\'" | awk \'{print $2}\' | sed s/://g| wc -l'
   diskAvailable=os.popen(noOfDisks).read().strip()
   print 'Total physical disk attached \n-----------------\n',diskAvailable

cmdLineArgs = getArgs()
displayServerInfo(cmdLineArgs.server)
