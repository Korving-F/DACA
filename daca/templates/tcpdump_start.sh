#!/bin/sh
# Source: https://stackoverflow.com/questions/61019058/why-doesnt-tcpdump-run-in-background
rm -f nohup.out
nohup /usr/sbin/tcpdump -ni eth0 -s 65535 -w file_result.pcap &

# Write tcpdump's PID to a file
echo $! > /var/run/tcpdump.pid