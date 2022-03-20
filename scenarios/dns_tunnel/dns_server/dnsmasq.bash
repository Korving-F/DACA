#!/bin/env bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y dnsmasq

systemctl stop systemd-resolved
systemctl disable systemd-resolved

DNS_SERVER="192.168.0.20"
cat << EOF > dnsmasq.conf
log-queries
log-facility=/var/log/dnsmasq.log
no-resolv
server=9.9.9.9
server=8.8.8.8
server=/attack/$DNS_SERVER
strict-order
EOF
