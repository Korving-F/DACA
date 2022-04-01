# DNS Tunnel

## Description
This directory contains DNS tunnel scenario description files.

Main documentation and datasets can be found in the [dedicated GitHub repository](https://github.com/Korving-F/dns-tunnel-dataset).

## Overview
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