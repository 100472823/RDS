#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
from functools import partial


class SingleSwitchTopo(Topo):
    'My single switch connected to n hosts.'

    def build(self, N=2):
        switch = self.addSwitch('s1')
        for hn in range(N):
            mac_suffix = format(hn + 1, '02x')
            mac_address = f'00:00:00:00:00:{mac_suffix}'
            host = self.addHost(f'h{hn+1}', ip='1.1.1.1', mac=mac_address)
            self.addLink(host, switch)


def simpleTestCLI():
    topo = SingleSwitchTopo(4)
    net = Mininet(topo,controller=partial(RemoteController, ip="127.0.0.1"),switch=partial(OVSSwitch, protocols="OpenFlow1"))
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTestCLI()
