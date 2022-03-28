# <a href="https://github.com/Korving-F/DACA"><img alt="DACA" src="/images/logo.svg" height="120"></a>
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://en.wikipedia.org/wiki/MIT_License)
[![Pipenv](https://img.shields.io/github/pipenv/locked/python-version/Korving-F/DACA)](https://github.com/pypa/pipenv)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Korving-F/daca)](https://github.com/Korving-F/DACA)

## Overview
![](data/simple_example_scenario/runthrough.gif)

## Quick Start

## Requirements
This project was created and tested using `python3.8`  
In addition to dependencies installable through pipenv one needs local installations of 

* [![Vagrant](https://img.shields.io/badge/vagrant-%231563FF.svg?style=for-the-badge&logo=vagrant&logoColor=white)](https://www.vagrantup.com/)

* [![VirtualBox](https://img.shields.io/static/v1?style=for-the-badge&message=VirtualBox&color=183A61&logo=VirtualBox&logoColor=FFFFFF&label=)](https://www.virtualbox.org/)
* [![Apache Kafka](https://img.shields.io/static/v1?style=for-the-badge&message=Apache+Kafka&color=231F20&logo=Apache+Kafka&logoColor=FFFFFF&label=)](https://kafka.apache.org/)
* [![Elasticsearch](https://img.shields.io/static/v1?style=for-the-badge&message=Elasticsearch&color=005571&logo=Elasticsearch&logoColor=FFFFFF&label=)](https://www.elastic.co/)


## Installation
This project uses pipenv for dependency management.
Installation instructions can be found [here](https://github.com/pypa/pipenv#installation).
```bash
pip3 install pipenv
pipenv install
```

```bash
vagrant plugin install vagrant-vbguest
vagrant plugin install vagrant-scp
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

### Multi-component scenario
```bash
scenarios/
├── web_attack_scenario           # Multi-component scenario.
│   ├── web_attack_scenario.yaml  # Main scenario file (same name as parent directory)
│   ├── component_webserver       # First webserver component with 2 instances.
│   │   ├── httpd.yaml            # 
│   │   ├── httpd_playbook        # Anisble playbook to provision httpd
│   │   ├── nginx.yaml            # 
│   │   └── nginx.bash            # Script to provision nginx
│   └── component_scanner         # Second component with two scanner subcomponents.
│       ├── nmap.yaml             # 
│       └── wpscan.yaml           # 
└── simple_scenario               # Single component scenario contained in a single file. 
    └── simple_scenario.yaml      # See below for a working example.
```

### Simple, single-file scenario
<details>
<summary>This scenario sets up a vulnerable webapp and runs some nmap scans against it.
It collects a tcpdump, raw log file and a shell recording as artifacts.</summary>
<p>

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
      val: >
        echo "[+] Installing dependencies";
        sudo apt-get update;
        sudo apt install -y python2.7 unzip nmap asciinema;

        echo "[+] Installing Vulnerable Web App Gruyère";
        wget http://google-gruyere.appspot.com/gruyere-code.zip -O /tmp/gruyere-code.zip;
        unzip /tmp/gruyere-code.zip -d /opt/gruyere-code;

    # Notice the Jinja2 template variable
    run:
      type: shell
      val: >
        echo "[+] Run webserver";
        set -x;
        sudo python2.7 /opt/gruyere-code/gruyere.py > /tmp/gruyere.log 2>&1 & sleep 1;
        "{{ variables.nmap }}";

    artifacts_to_collect:
      - type: pcap
        val:  ["tcpdump -i any -n -t -w /tmp/web.pcap port 8008"]
      - type: files
        val: ["/tmp/gruyere.log", "/tmp/*.cast", "/tmp/*.pcap"]
      - type: cli_recording
        val: ["/tmp/nmap.cast"]

# These entries are substituted for the Jinja2 tempate variable in the run section.
variables:
  - nmap:
    - nmap -sV -p 8008 --script=http-enum 127.0.0.1
    - nmap -p8008 --script http-waf-detect 127.0.0.1
    - nmap -p8008 --script http-wordpress-users 127.0.0.1
```

</p>
</details>


## Architecture

## Future Development
* Docker / Docker-Compose (Not yet supported #24) [![Docker](https://img.shields.io/badge/docker-%232496ED.svg?&style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
* Terraform (Not yet supported #11) [![Terraform](https://img.shields.io/static/v1?style=for-the-badge&message=Terraform&color=7B42BC&logo=Terraform&logoColor=FFFFFF&label=)](https://www.terraform.io/)

## Run Tests
```bash
python -m pytest
```
