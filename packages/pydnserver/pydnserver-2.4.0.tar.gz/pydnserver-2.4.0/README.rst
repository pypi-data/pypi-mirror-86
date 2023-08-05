
PyDNServer
========================

Provides a very simple DNS server.  It provides the following functionality:
* Resolves hostnames to IP addresses.  (A record lookups)
* Resolves hostnames to hostnames. (CNAME lookups)


To start up a DNS server::

    from pydnserver import DNSServer

    ip = u'192.168.0.10  # Set this to the IP address of your network interface.

    dns = DNSServer(interface=ip, port=53)
    dns.start()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        dns.stop()

This starts a bare bones DNS server that will forward all requests to the google DNS servers (8.8.8.8, 8.8.4.4).

Configuration can currently be managed using the configurationutil.Configuration interface.

The configuration is dynamic. If it is changed, it will be reflected in the next request.
