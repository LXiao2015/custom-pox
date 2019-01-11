import subprocess
import sys
import distribute as dis
import global_para as gl
import pox.openflow.libopenflow_01 as of

pathList = []
demandList = []

# call algorithm to form paths
def formPath():
    print("System booted. Do you want to add more chains? (Y or N)")
    r = raw_input()
    if r == "N" or r == "n" or r == "No" or r == "NO":
        '''
        try:
            ret = subprocess.check_output("./../cppalg/main", shell=True)
            print  'res:', ret
        except subprocess.CalledProcessError, exc:
            print 'returncode:', exc.returncode
            print 'cmd:', exc.cmd
            print 'output:', exc.output

        with open('/home/ubuntu/cppalg/output/result.txt', 'w') as out:
            out.write(ret)
        '''
        print("Get results...")
        pathList = readIn()
        dis.sendFlowTable(pathList)
        print("Do you want to add more chains? (Y or N)")
        r = raw_input()
    while r == "Y" or r == "y" or r == "yes" or r == "Yes" or r == "YES":
        print("One line per session, Enter the source node, sink node, service type and bandwidth in turn, separated by spaces.")
        print("Type # to end the input.")
        f = open('/home/ubuntu/cppalg/input/input_chains.txt', 'w')
        r = raw_input()
        while r != '#':
	    f.write(r + '\n')
	    r = raw_input()
        f.close()
        print("All input received. MDP algorithm start...")
        
        try:
            ret = subprocess.check_output("./../cppalg/main", shell=True)
            print  'res:', ret
        except subprocess.CalledProcessError, exc:
            print 'returncode:', exc.returncode
            print 'cmd:', exc.cmd
            print 'output:', exc.output

        out = open('/home/ubuntu/cppalg/output/result.txt', 'w')
        out.write(ret)
        out.close()
        
        print("Get results...")
        pathList = readIn()
        dis.sendFlowTable(pathList)
        print("Do you want to add more chains? (Y or N)")
        r = raw_input()

def findPath(in_port, sw, src_ip, dst_ip):
    sw_node = gl.hostNum + sw
    print("sw_node: ", sw_node)
    src_ip_list = src_ip.split('.')
    dst_ip_list = dst_ip.split('.')
    if len(src_ip_list) != 4 or len(dst_ip_list) != 4:
        print("IP resolve ERROR! ", src_ip_list, dst_ip_list)
        return of.OFPP_NONE
    src_node = src_ip_list[3]
    dst_node = dst_ip_list[3]
    pathList = readIn()
    for p in pathList:
        if p[0] == src_node and p[len(p) - 1] == dst_node:
            for i in range(1, len(p) - 1):
                if p[i] == str(sw_node):
                    # curNode, preNode, nextNode, dst, priority
                    print("Send flow table between %s - %s - %s." % (p[i-1], p[i], p[i+1]))
                    dis.sendToSwitchByNodeNumber(p[i], p[i - 1], p[i + 1], src_node, dst_node, 1)
                    dis.sendToSwitchByNodeNumber(p[i], p[i + 1], p[i - 1], dst_node, src_node, 1)
                    return dis.getPort(str(sw_node), p[i + 1])
        if p[0] == dst_node and p[len(p) - 1] == src_node:
            p.reverse()
            for i in range(1, len(p) - 1):
                if p[i] == str(sw_node):
                    # curNode, preNode, nextNode, dst, priority
                    print("Send flow table between %s - %s - %s." % (p[i-1], p[i], p[i+1]))
                    dis.sendToSwitchByNodeNumber(p[i], p[i - 1], p[i + 1], src_node, dst_node, 1)
                    dis.sendToSwitchByNodeNumber(p[i], p[i + 1], p[i - 1], dst_node, src_node, 1)
                    return dis.getPort(str(sw_node), p[i + 1])
    return of.OFPP_NONE

# read paths from output file
def readIn():
    demandList = []
    pathList = []
    with open('/home/ubuntu/cppalg/output/demandAndPath.txt', 'r') as f:
	for line in f:
            if line == "":
                print("Format error in demandAndPath.txt file!")
                continue
            res = line.split()
            demandList.append(res[0])
	    pathList.append(res[1:])
    # print(demandList)
    print(pathList)
    return pathList
    # dis.sendFlowTable(pathList)
