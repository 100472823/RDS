#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
from functools import partial






class Hito1Topo(Topo):
    'My single switch connected to n hosts.'

    def build(self, N=2):
        switch = self.addSwitch('s1', mac='70:88:99:00:00:01', ip='10.0.0.1/24')
        host1 = self.addHost('h1', ip='10.0.0.2/24', mac='00:00:00:00:00:01')
        host2 = self.addHost('h2', ip='10.0.1.2/24', mac='00:00:00:00:00:02')
        
        self.addLink(host1, switch, intfName2='s1-eth1')
        self.addLink(host2, switch, intfName2='s1-eth2')


def configureStaticARP(host, ip, mac):
    # Establecer una entrada ARP estática en el host
    host.setARP(ip=ip, mac=mac)




def simpleTestCLI():
    topo = Hito1Topo(4)
    net = Mininet(topo,controller=partial(RemoteController, ip="127.0.0.1"),switch=partial(OVSSwitch, protocols="OpenFlow13"))
    net.start()
    h1 = net.get("h1")
    h2 = net.get("h2")
    configureStaticARP(h1,ip='10.0.0.1', mac='70:88:99:00:00:01')
    configureStaticARP(h2,ip='10.0.1.1',mac='70:88:99:10:00:02' )
    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTestCLI()







