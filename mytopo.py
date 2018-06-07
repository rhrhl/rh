"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        host3 = self.addHost( 'h3' )
		host4 = self.addHost( 'h4' )
		host5 = self.addHost( 'h5' )
		host6 = self.addHost( 'h6' )
		host7 = self.addHost( 'h7' )
		host8 = self.addHost( 'h8' )
		Switch1 = self.addSwitch( 's1' )
        Switch2 = self.addSwitch( 's2' )
		Switch3 = self.addSwitch( 's3' )
		Switch4 = self.addSwitch( 's4' )
		Switch5 = self.addSwitch( 's5' )
		Switch6 = self.addSwitch( 's6' )
		Switch7 = self.addSwitch( 's7')
        # Add links
        self.addLink( Switch1, Switch2 )
        self.addLink( Switch1, Switch3 )
        self.addLink( Switch2, Switch4 )
		self.addLink( Switch2, Switch5 )
		self.addLink( Switch3, Switch6 )
		self.addLink( Switch3, Switch7)
		self.addLink( Switch4, host1 )
		self.addLink( Switch4, host2 )
		self.addLink( Switch5, host3 )
		self.addLink( Switch5, host4 )
		self.addLink( Switch6, host5 )
		self.addLink( Switch6, host6 )
		self.addLink( Switch7, host7 )
		self.addLink( Switch7, host8 )


topos = { 'mytopo': ( lambda: MyTopo() ) }
