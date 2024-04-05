#!/usr/bin/env python3
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
def simpleTestCLI():
	topo = SingleSwitchTopo(4)
	net = Mininet(topo)
	net.start()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	# Tell mininet to print useful information
	setLogLevel('info')
	simpleTestCLI()
