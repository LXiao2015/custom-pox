import subprocess
import sys
import distribute as dis

pathList = []
demandList = []

# call algorithm to form paths
def formPath():
    print("System booted. Do you want to add more chains? (Y or N)")
    r = raw_input()
    while r == "Y" or r == "y" or r == "yes" or r == "Yes" or r == "YES":
        print("One line per session, Enter the source node, sink node, service type and bandwidth in turn, separated by spaces.")
        print("Type # to end the input.")
        r = raw_input()
        f = open('/home/ubuntu/cppalg/input/input_chains.txt', 'w')
        while r != '#':
			f.write(r + '\n')
			r = raw_input()
		# the return value contains lots of messages (choices, paths...)
        f.close()
        print("All input received. MDP algorithm start...")
        try:
            ret = subprocess.check_output("./../cppalg/main", shell=True)
            print  'res:', ret
        except subprocess.CalledProcessError, exc:
            print 'returncode:', exc.returncode
            print 'cmd:', exc.cmd
            print 'output:', exc.output

        with open('/home/ubuntu/cppalg/output/result.txt', 'w') as out:
            out.write(ret)
        print("Get results...")
        readIn()
        print("Do you want to add more chains? (Y or N)")
        r = raw_input()

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
