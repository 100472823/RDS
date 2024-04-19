#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
from functools import partial






class Hito1Topo(Topo):
    'My single switch connected to n hosts.'

    def build(self):
            switch = self.addSwitch('s1')
            host1 = self.addHost('h1', ip='10.0.0.2/24', mac='00:00:00:00:00:01')
            host2 = self.addHost('h2', ip='10.0.1.2/24', mac='00:00:00:00:00:02')
        
            # Conectar h1 a s1-eth1 y h2 a s1-eth2
            self.addLink(host1, switch, intfName2='s1-eth1')
            self.addLink(host2, switch, intfName2='s1-eth2')
    



def simpleTestCLI():
    topo = Hito1Topo()
    net = Mininet(topo,controller=partial(RemoteController, ip="127.0.0.1"),switch=partial(OVSSwitch, protocols="OpenFlow13"))
    net.start()
    
   # s1 = net.get('s1')
   # s1.setIP('10.0.0.1/24', intf='s1-eth1')
   # s1.setMAC('70:88:99:00:00:01', intf='s1-eth1')
   # s1.setIP('10.0.1.1/24', intf='s1-eth2')
   # s1.setMAC('70:88:99:10:00:02', intf='s1-eth2')

     # Obtener referencias a los hosts
    h1 = net.get('h1')
    h2 = net.get('h2')

    # Configurar rutas y entradas ARP estáticas
    h1.cmd('route add default gw 10.0.0.1')
    h2.cmd('route add default gw 10.0.1.1')

    h1.setARP('10.0.0.1', '70:88:99:00:00:01')  # Establecer entrada ARP estática en h1 para h2
    h2.setARP('10.0.1.1', '70:88:99:10:00:02')  # Establecer entrada ARP estática en h2 para h1


    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTestCLI()







