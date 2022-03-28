# <a href="https://github.com/Korving-F/DACA"><img alt="DACA" src="/images/logo.svg" height="120"></a>
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://en.wikipedia.org/wiki/MIT_License)
[![Pipenv](https://img.shields.io/github/pipenv/locked/python-version/Korving-F/DACA)](https://github.com/pypa/pipenv)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Korving-F/daca)](https://github.com/Korving-F/DACA)


## Table of Contents
* [Overview](#overview)
* [Requirements](#requirements)
* [Installation](#installation)
* [Writing Scenarios](#writing-scenarios)
    * [Single file](#simple-single-file-scenario)
    * [Multi-component](#multi-component-scenario)
* [Architecture](#architecture)
* [Data Sets](#data-sets)  
* [Future Development](#future-development)  
* [Run Tests](#run-tests)  

## Overview
![](data/simple_example_scenario/runthrough.gif)

## Requirements
This project was created and tested using `python3.8`.
In addition to dependencies installable through pipenv one needs local installation of:

Provisioner:
* [![Vagrant](https://img.shields.io/badge/vagrant-%231563FF.svg?style=for-the-badge&logo=vagrant&logoColor=white)](https://www.vagrantup.com/)
* [![VirtualBox](https://img.shields.io/static/v1?style=for-the-badge&message=VirtualBox&color=183A61&logo=VirtualBox&logoColor=FFFFFF&label=)](https://www.virtualbox.org/)
![VMware](https://img.shields.io/static/v1?style=for-the-badge&message=VMware&color=607078&logo=VMware&logoColor=FFFFFF&label=)

If you want to make use of the `kafka` or `elasticsearch` output you need to install these  
* [![Apache Kafka](https://img.shields.io/static/v1?style=for-the-badge&message=Apache+Kafka&color=231F20&logo=Apache+Kafka&logoColor=FFFFFF&label=)](https://kafka.apache.org/)
* [![Elasticsearch](https://img.shields.io/static/v1?style=for-the-badge&message=Elasticsearch&color=005571&logo=Elasticsearch&logoColor=FFFFFF&label=)](https://www.elastic.co/)

## Installation
This project uses pipenv for dependency management.
Installation instructions can also be found [here](https://github.com/pypa/pipenv#installation).
```bash
pip3 install pipenv
pipenv install
```
The `vagrant-scp` module is used to collect data from VMs and needs to be installed as well:
```bash
vagrant plugin install vagrant-vbguest
vagrant plugin install vagrant-scp
```

## Writing Scenarios
Out-of-the-box scenarios are listed within the `./scenarios` directory and can be used as a reference.
Scenario files are found when they have the same name as their scenario directory.

Scenarios consist of components, the simplest type of Scenario has only a single component.
Each component has 2 main sections:
1. **setup**: this contains installation / provisioning steps.
2. **run**: this contains runtime commands.

The Setup phase builds/snapshots the VMs or Docker containers, initializing the Scenario.
The run section is evaluated on Scenario execution.

In the background network traffic can be captured and logs can be streamed to a Kafka broker or Elasticsearch cluster.
Raw logs or other artifacts can be gathered after-the-fact as well.

Scenario files are interpreted as [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) files which allow for 

### Simple, single-file scenario
<details>
<summary>This scenario sets up a vulnerable webapp and runs some nmap scans against it.
It collects a tcpdump, raw log file and a <a href="https://asciinema.org/">asciinema</a> terminal session recording as artifacts.
The tool also writes all needed files to reproduce the scenario to a dedicated directory.
See also <a href="https://github.com/Korving-F/DACA/tree/main/data/simple_example_scenario">here</a> for the output of this particular example.</summary>
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



## Architecture

## Data Sets

## Future Development
Many scenarios lend themselves to also be run on Docker (faster than current VM-based approach) while new scenarios could also be written for the cloud through Terraform (AWS, Google, Azure) which would allow generation/collection of cloud-native datasets.
* [![Docker](https://img.shields.io/badge/docker-%232496ED.svg?&style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) (Not yet supported #24) 
* [![Terraform](https://img.shields.io/static/v1?style=for-the-badge&message=Terraform&color=7B42BC&logo=Terraform&logoColor=FFFFFF&label=)](https://www.terraform.io/) (Not yet supported #11) 

Currently the [local Anisble provisioner](https://www.vagrantup.com/docs/provisioning/ansible_local) is used to initialize VMs, which installs / runs Ansible from within the VM. However ideally an installation on the Host is used.
* [![Ansible](https://img.shields.io/badge/ansible-%231A1918.svg?style=for-the-badge&logo=ansible&logoColor=white)](https://www.ansible.com/)  (Not yet supported #31)

## Run Tests
```bash
python -m pytest
```
