# <a href="https://github.com/Korving-F/DACA"><img alt="DACA" src="/images/logo.svg" height="120"></a>
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://en.wikipedia.org/wiki/MIT_License)
[![Pipenv](https://img.shields.io/github/pipenv/locked/python-version/Korving-F/DACA)](https://github.com/pypa/pipenv)

## Overview


## Quick Start

## Requirements
In addition to dependencies installable through pipenv one needs local installations of 

* Vagrant
* Docker
* Terraform
* Ansible

## Installation
This project uses pipenv for dependency management.
Installation instructions can be found [here](https://github.com/pypa/pipenv#installation).
```bash
pip3 install pipenv
pipenv install
```

## Writing Scenarios
Out-of-the-box scenarios are listed within the `./scenarios` directory.
Scenario files are found when they have the same name as their scenario directory.

Scenarios consist of components, the simplest type of Scenario has only a single one.
Each component has 2 main sections:
1. **setup**: this contains installation / configuration steps.
2. **run**: this contains runtime commands.

Setup phase builds/snapshots the VMs or Docker containers, initializing the Scenario.
The run section is evaluated on Scenario execution.

In the background network traffic can be captured as well as logs can be streamed to a kafka broker.
Raw logs or other artifacts can be gathered as well.

```bash
scenarios/
├── web_attack_scenario           # 
│   ├── web_attack_scenario.yaml  # 
│   ├── component_webserver       # 
│   │   ├── httpd.yaml            # 
│   │   └── nginx.yaml            # 
│   └── component_scanner         # 
│       ├── nmap.yaml             # 
│       └── wpscan.yaml           # 
└── simple_scenario               # 
    └── simple_scenario.yaml      # 
```

```yaml
# simple_scenario.yaml
name: "Simple example Scenario"
description: |
  "This Scenario sets up a vulnerable web application and runs multiple NMAP scans against it."
provisioner: vagrant
use_default_templates: True

components:
  - name: main_server
    description: Main Ubuntu machine used in this example scenario
    image: ubuntu/focal64
    setup:
      type: shell
      val: |
        echo "[+] Installing dependencies"
        sudo apt-get update
        sudo apt install -y unzip nmap

        echo "[+] Installing Vulnerable Web App Gruyère"
        wget http://google-gruyere.appspot.com/gruyere-code.zip -O /tmp/gruyere-code.zip
        unzip /tmp/gruyere-code.zip -d /opt/gruyere-code

        echo "[+] Setting up logfile for Vulnerable Web App"
        sed -i 's/print >>sys.stderr, message/open("\/tmp\/gruyere.log","a+").writelines(list(message))/g' /opt/gruyere-code/gruyere.py

    # Notice the Jinja2 template variable
    run:
      type: shell
      val: |
        echo "[+] Run webserver"
        python2.7 /opt/gruyere-code/gruyere.py &
        {{ variables.nmap }}

    artifacts_to_collect:
      - type: pcap
        val:  ["place BPF filter here"]
      - type: files
        val: ["/tmp/gruyere.log"]

# These entries are substituted for the Jinja2 tempate variable in the run section.
variables:
  - name: nmap
    val:
      - nmap -sV --script=http-enum 127.0.0.1:8008
      - nmap -p8008 --script http-waf-detect 127.0.0.1
      - nmap -p8008 --script http-wordpress-users 127.0.0.1
```

## Architecture

## Contribute


## Run Tests
```bash
python -m pytest
```
