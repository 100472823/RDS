# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import igmplib
from ryu.lib.dpid import str_to_dpid
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.app import simple_switch_13


class MyApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'igmplib': igmplib.IgmpLib}

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self._snoop = kwargs['igmplib']
        self._snoop.set_querier_mode(
            dpid=str_to_dpid('0000000000000001'), server_port=2)

    @set_ev_cls(igmplib.EventPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(igmplib.EventMulticastGroupStateChanged,
                MAIN_DISPATCHER)
    def _status_changed(self, ev):
        msg = {
            igmplib.MG_GROUP_ADDED: 'Multicast Group Added',
            igmplib.MG_MEMBER_CHANGED: 'Multicast Group Member Changed',
            igmplib.MG_GROUP_REMOVED: 'Multicast Group Removed',
        }
        self.logger.info("%s: [%s] querier:[%s] hosts:%s",
                         msg.get(ev.reason), ev.address, ev.src,
                         ev.dsts)
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
# install table-miss flow entry
#
# We specify NO BUFFER to max_len of the output action due to
# OVS bug. At this moment, if we specify a lesser number, e.g.,
# 128, OVS will send Packet-In with invalid buffer_id and
# truncated packet data. In that case, we cannot output packets
# correctly. The bug has been fixed in OVS v2.1.0.
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
        ofproto.OFPCML_NO_BUFFER)]
        match = parser.OFPMatch()
        self.add_flow(datapath, 0, match, actions)


    def add_flow(self, datapath, priority, match, actions,
                buffer_id=None, idle_timeout=0, table_id=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        cookie = cookie_mask = 0
        hard_timeout = 0
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
        actions)]
        if buffer_id is not None:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    idle_timeout=idle_timeout,
                                    hard_timeout=hard_timeout,
                                    priority=priority,
                                    table_id = table_id,
                                    match=match, instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath,
                                        idle_timeout=idle_timeout,
                                        hard_timeout=hard_timeout,
                                        priority=priority,
                                        table_id = table_id,
                                        match=match, instructions=inst)
            
# If you hit this you might want to increase
# the "miss_send_length" of your switch
    if ev.msg.msg_len < ev.msg.total_len:
        self.logger.debug(
            f"packet truncated: only {ev.msg.msg_len} of {ev.msg.total_len} bytes")
        


    msg = ev.msg
    datapath = msg.datapath
    ofproto = datapath.ofproto
    parser = datapath.ofproto_parser
    in_port = msg.match['in_port']
    
    pkt = packet.Packet(msg.data)
    eth = pkt.get_protocols(ethernet.ethernet)[0]
    if eth.ethertype == ether_types.ETH_TYPE_LLDP:
        # ignore lldp packet
        return
    dst = eth.dst
    src = eth.src
    dpid = datapath.id
    self.mac_to_port.setdefault(dpid, {})
    self.logger.info(
        f"in: {dpid} <{eth.ethertype:04x}> {src} {dst} {in_port}")
    # learn a mac address to avoid FLOOD next time.
    self.mac_to_port[dpid][src] = in_port