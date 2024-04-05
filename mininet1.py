#!/usr/bin/env python3
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
def simpleTest():
	'Create and test a simple network'
	topo = SingleSwitchTopo(4)
	net = Mininet(topo)
	net.start()
	print('Dumping host connections')
	dumpNodeConnections(net.hosts)
	print('Testing network connectivity')
	net.pingAll()
	net.stop()
if __name__ == '__main__':
	# Tell mininet to print useful information
	setLogLevel('info')
	simpleTest()
