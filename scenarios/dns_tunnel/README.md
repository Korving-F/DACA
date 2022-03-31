# DNS Tunnel

## Description
This directory contains DNS tunnel scenario description files.

## Components
### Overview
```
dns_tunnel/                 # Main scenario directory
├── dns_servers             # 
│   ├── bind9.yaml          # Implementation specific parameters. e.g. Installation commands, log file locations.
│   ├── bind9_playbook      # Ansible playbook to provision the service
│   └── dnsmasq.yaml        # 
├── dns_tunnels             # Scenario component: DNS tunnelling software
│   ├── dnscat.yaml         # Implementation specific parameters. e.g. Installation commands, variables, initiating commands.
│   └── iodine.yaml         # 
└── dns_tunnel.yaml.j2      # Main scenario description file.
```

### DNS Servers
* <a href="https://thekelleys.org.uk/dnsmasq/doc.html">Dnsmasq</a>
* <a href="https://www.isc.org/bind/">Bind9</a>
* <a href="https://www.powerdns.com/">PowerDNS</a>
* <a href="https://coredns.io/">CoreDNS</a>

### DNS Tunnel
* <a href="https://github.com/yarrick/iodine">Iodine</a>
* <a href="https://github.com/iagox86/dnscat2">DNScat</a>
* <a href="https://github.com/alex-sector/dns2tcp">dns2tcp</a>

## Overview
# <a href="https://github.com/Korving-F/iodine-log-analysis"><img alt="Iodine DNS Tunnel" src="tunnel_init.png" height="400"></a>

## References
* https://github.com/Korving-F/iodine-log-analysis
