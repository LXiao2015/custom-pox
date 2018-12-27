#!/usr/bin/python
#coding=utf-8 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.link import TCLink
import global_para as gl
import lru
import json
# from global_para import gl

h_s = dict(bw=80)
s_s = dict(bw=40)

gl._init()

class Node45Topo(Topo):
        def __init__(self, **opts):
                Topo.__init__(self, **opts)

                hostNum = gl.hostNum
                switchNum = gl.switchNum
                nfNum = gl.nfNum

                host = []
                for i in range(1, hostNum + 1):
                        host.append(self.addHost( 'h%s' % i, ip='10.0.0.%s' % i ))

                switch = []
                for i in range(1, switchNum + 1):
                        switch.append(self.addSwitch( 's%s' % i, ip='10.0.0.%s' % (i + hostNum) ))

                nf = []
                for i in range(1, nfNum + 1):
                        nf.append(self.addSwitch( 'n%s' % (i + switchNum), ip='10.0.0.%s' % (i + hostNum + switchNum) ))
                '''                
                print(host)
                print(switch)
                print(nf)
                '''
                # 连接边缘交换机与 host
                i = 0
                for j in range(9):    # [0, 9)
                        for d in range(3):    # [0, 3)
                                self.addLink( host[i], switch[j], port1=1, port2=d+1, **h_s )
                                gl.set_links(i + 1, j + hostNum + 1, 1)
                                gl.set_links(j + hostNum + 1, i + 1, d + 1)
                                i += 1

		# 连接边缘交换机与核心交换机
                i = 0
                for j in range(9, 12):    # s10 ~ s12
                        for d in range(3):
                                self.addLink( switch[i], switch[j], port1=4, port2=d+1, **s_s )
                                gl.set_links(i + hostNum + 1, j + hostNum + 1, 4)
                                gl.set_links(j + hostNum + 1, i + hostNum + 1, d + 1)
                                i += 1

		# 连接核心交换机
                self.addLink( switch[9], switch[10], port1=4, port2=4, **s_s )
                gl.set_links(9 + hostNum + 1, 10 + hostNum + 1, 4)
                gl.set_links(10 + hostNum + 1, 9 + hostNum + 1, 4)
                self.addLink( switch[9], switch[11], port1=5, port2=4, **s_s )
                gl.set_links(9 + hostNum + 1, 11 + hostNum + 1, 5)
                gl.set_links(11 + hostNum + 1, 9 + hostNum + 1, 4)
                self.addLink( switch[9], switch[12], port1=6, port2=1, **s_s )
                gl.set_links(9 + hostNum + 1, 12 + hostNum + 1, 6)
                gl.set_links(12 + hostNum + 1, 9 + hostNum + 1, 1)
                self.addLink( switch[10], switch[11], port1=5, port2=5, **s_s )
                gl.set_links(10 + hostNum + 1, 11 + hostNum + 1, 5)
                gl.set_links(11 + hostNum + 1, 10 + hostNum + 1, 5)
                self.addLink( switch[10], switch[12], port1=6, port2=2, **s_s )
                gl.set_links(10 + hostNum + 1, 12 + hostNum + 1, 6)
                gl.set_links(12 + hostNum + 1, 10 + hostNum + 1, 2)
                self.addLink( switch[11], switch[12], port1=6, port2=3, **s_s )
                gl.set_links(11 + hostNum + 1, 12 + hostNum + 1, 6)
                gl.set_links(12 + hostNum + 1, 11 + hostNum + 1, 3)

		# 连接 nf
                self.addLink( nf[0], switch[12], port1=1, port2=4, **h_s )
                gl.set_links(0 + hostNum + switchNum + 1, 12 + hostNum + 1, 1)
                gl.set_links(12 + hostNum + 1, 0 + hostNum + switchNum + 1, 4)
                self.addLink( nf[1], switch[2], port1=1, port2=5, **h_s )
                gl.set_links(1 + hostNum + switchNum + 1, 2 + hostNum + 1, 1)
                gl.set_links(2 + hostNum + 1, 1 + hostNum + switchNum + 1, 5)
                self.addLink( nf[2], switch[5], port1=1, port2=5, **h_s )
                gl.set_links(2 + hostNum + switchNum + 1, 5 + hostNum + 1, 1)
                gl.set_links(5 + hostNum + 1, 2 + hostNum + switchNum + 1, 5)
                self.addLink( nf[3], switch[8], port1=1, port2=5, **h_s )
                gl.set_links(3 + hostNum + switchNum + 1, 8 + hostNum + 1, 1)
                gl.set_links(8 + hostNum + 1, 3 + hostNum + switchNum + 1, 5)
                self.addLink( nf[4], switch[12], port1=1, port2=5, **h_s )
                gl.set_links(4 + hostNum + switchNum + 1, 12 + hostNum + 1, 1)
                gl.set_links(12 + hostNum + 1, 4 + hostNum + switchNum + 1, 5)

                gl.del_node(0)
                # gl.print_links()
                jsondata = json.dumps(gl.graph)
                f = open("port.json", "w")
                f.writelines(jsondata)
                # print("gl.graph[33][16]: ", gl.graph[33][16])
                # print(self.linksBetween( host[1], switch[0] ))

 
def simpleTest():
        topo = Node45Topo()
        net = Mininet(topo, link=TCLink, autoStaticArp=True)    #主要类来创建和管理网络
        mycontroller = RemoteController("c0", ip="127.0.0.1", port=6633)    #创建远程控制器
        net.controllers = [mycontroller]
        net.start()    #启动您的拓扑网络
        print "***Dumping host connections"
        dumpNodeConnections(net.hosts)       #转存文件连接
        # print "Testing network connectivity"     
        # net.pingAll()    #所有节点彼此测试互连
        CLI(net)		#进入mininet>提示符 
        net.stop()       #停止您的网络

 		
if __name__ == '__main__':
        setLogLevel('info')  # 设置 Mininet 默认输出级别，设置 info 它将提供一些有用的信息
	simpleTest()
        print("Removing...")
	for i in range(1, gl.switchNum + 1):
	    remove_rules('s%d' % i)
