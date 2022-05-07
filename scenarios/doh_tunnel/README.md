# DNS Tunnel over DoH

## Description

C2 and File transfer


## Overview
```
doh/                        # Main scenario directory
```


```bash
# Install GO
curl -OL https://golang.org/dl/go1.16.7.linux-amd64.tar.gz
sudo tar -C /usr/local -xvf go1.16.7.linux-amd64.tar.gz
#sudo nano ~/.profile
# NB LINE IN FILE / environment
export PATH=$PATH:/usr/local/go/bin
#source ~/.profile
go version
mkdir ~/gopath
export GOPATH=~/gopath


git clone https://github.com/m13253/dns-over-https.git
cd dns-over-https/
make
sudo make install
sudo systemctl stop systemd-resolved
sudo systemctl start doh-client.service
sudo systemctl status doh-client.service

sudo systemctl status doh-client.service
dig www.google.com


# Configfile
/etc/dns-over-https/doh-client.conf
/etc/dns-over-https/doh-server.conf
```