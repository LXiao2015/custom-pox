import subprocess
import sys
import distribute as dis

pathList = []
demandList = []

# call algorithm to form paths
def formPath():
    # the return value contains lots of messages (choices, paths...)
    print("MC algorithm start...")
    # ret = subprocess.check_output("./../cppalg/main", shell=True)
    print("Get results...")
    readIn()

# read paths from output file
def readIn():
    with open('/home/ubuntu/cppalg/output/demandAndPath.txt', 'r') as f:
	for line in f:
            if line == "":
                print("Format error in demandAndPath.txt file!")
                continue
            res = line.split()
            demandList.append(res[0])
	    pathList.append(res[1:])
    print(demandList)
    print(pathList)
    dis.sendFlowTable(pathList)
