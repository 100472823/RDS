#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI


class SingleSwitchTopo(Topo):
	'My single switch connected to n hosts.'

	def build(self, N=2):
		switch = self.addSwitch('s1')
		for hn in range(N):		   
			 host = self.addHost(f'h{hn+1}',ip='1.1.1.1')
			self.addLink(host, switch)

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
