#coding=utf-8

from pox.core import core
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr
import pox.lib.packet as pkt
import pox.openflow.libopenflow_01 as of
import json

def readInPortMapping():
    f = open("/home/ubuntu/pox/pox/openflow/port.json", "r")
    global graph
    graph = json.loads(f.readline())
    f.close()

import global_para as gl
# from global_para import gl

def sendFlowTable(pathList):
    readInPortMapping()
    print(graph)
    sendSFCFlowTable(pathList)
    # sendARPFlowTable(pathList)
    # conn = core.openflow.connections.keys()

def sendSFCFlowTable(pathList):
    print("Send SFC Flow Tables...")
    for path in pathList:
        pathLen = len(path)
        # print("path length: %d" % pathLen)
        for i in range(1, pathLen - 1):
            # curNode, preNode, nextNode, dst
            sendToSwitchByNodeNumber(path[i], path[i - 1], path[i + 1], path[0], path[pathLen - 1])
            sendToSwitchByNodeNumber(path[i], path[i + 1], path[i - 1], path[pathLen - 1], path[0])

'''
def sendARPFlowTable(pathList):
    print("Send ARP Flow Tables...")    
    pathLen = len(path)
    for path in pathList:
	sendToEdgeSwitch(path[1], path[0], path[pathLen - 1])
'''

def getPort(sw, neighbor):
    if int(sw) > gl.hostNum + gl.switchNum + gl.nfNum or int(sw) <= 0:
        print("Wrong node number! sw: %s" % sw)
    if neighbor <= 0:
        print("Wrong node number! neighbor: %s" % neighbor)
    return graph[sw][neighbor]

def sendToSwitchByNodeNumber(sw, fr, to, src, dst):
    src_ip = "10.0.0." + src
    dst_ip = "10.0.0." + dst
    in_port = getPort(sw, fr)
    out_port = getPort(sw, to)
    sw_no = int(sw) - gl.hostNum

    # ICMP
    msg_icmp = of.ofp_flow_mod()
    msg_icmp.priority = 3    # 数字越大, 优先级越高
    msg_icmp.match.dl_type = 0x0800
    msg_icmp.match.nw_proto = 1
    msg_icmp.match.nw_src = src_ip
    msg_icmp.match.nw_dst = dst_ip
    msg_icmp.match.in_port = in_port
    msg_icmp.actions.append(of.ofp_action_output(port = out_port))

    core.openflow.connections[sw_no].send(msg_icmp)

'''
def sendToEdgeSwitch(edge, src, dst):
    src_ip = "10.0.0." + src
    dst_ip = "10.0.0." + dst
    in_port = getPort(sw, src)
    sw_no = int(sw) - gl.hostNum

    # ARP
    msg_arp = of.ofp_flow_mod()
    msg_arp.priority = 3    # 数字越大, 优先级越高, 0~65535
    msg_arp.match.dl_type = 0x0806
    msg_arp.match.nw_src = src_ip
    msg_arp.match.nw_dst = dst_ip
    msg_arp.match.in_port = in_port
    msg_arp.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))    # 发给控制器

    core.openflow.connections[sw_no].send(msg_arp)
'''
