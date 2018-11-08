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
    print("Test for graph.")
    readInPortMapping()
    print(graph)
    conn = core.openflow.connections.keys()
    for path in pathList:
        pathLen = len(path)
        # print("path length: %d" % pathLen)
        for i in range(1, pathLen - 1):
            # curNode, preNode, nextNode, dst
            sendToSwitchByNodeNumber(path[i], path[i - 1], path[i + 1], path[0], path[pathLen - 1])
            sendToSwitchByNodeNumber(path[i], path[i + 1], path[i - 1], path[pathLen - 1], path[0])

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

    msg = of.ofp_flow_mod()
    msg.priority = 3    # 数字越大, 优先级越高
    msg.match.dl_type = pkt.ethernet.IP_TYPE
    msg.match.nw_src = src_ip
    msg.match.nw_dst = dst_ip
    msg.match.in_port = in_port
    msg.actions.append(of.ofp_action_output(port = out_port))

    # print("Send flow table: %s, %s, %d, %d" % (src_ip, dst_ip, in_port, out_port))
    core.openflow.connections[sw_no].send(msg)
