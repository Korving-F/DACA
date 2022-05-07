#!/bin/bash
echo "[+] Installing NGINX as proxy"
sudo add-apt-repository ppa:ondrej/nginx -y
sudo apt -y install nginx-full

# Create self-signed certificate
sudo openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
    -subj "/C=EE/ST=Harjumaa/L=Tallinn/O=TalTech/CN=192.168.0.10" \
    -keyout /etc/ssl/private/192.168.0.10.key -out /etc/ssl/certs/192.168.0.10.crt

# Configure NGINX
cat << EOF > /etc/nginx/sites-available/dns-over-https
upstream dns-backend {
    server 127.0.0.1:8053;
}
server {
        listen 443 ssl;
        server_name 192.168.0.10;

        ssl_certificate     /etc/ssl/certs/192.168.0.10.crt;
        ssl_certificate_key /etc/ssl/private/192.168.0.10.key;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
        ssl_ciphers         HIGH:!aNULL:!MD5;

        root /var/www/html/dns;
        access_log /var/log/nginx/dns.access.log;
        location /dns-query {
                proxy_set_header X-Real-IP \$remote_addr;
                proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                proxy_set_header Host \$http_host;
                proxy_set_header X-NginX-Proxy true;
                proxy_http_version 1.1;
                proxy_set_header Upgrade \$http_upgrade;
                proxy_redirect off;
                proxy_set_header X-Forwarded-Proto \$scheme;
                proxy_read_timeout 86400;
                proxy_pass http://dns-backend/dns-query ;
                
        }
}
EOF

rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/dns-over-https /etc/nginx/sites-enabled/
sudo systemctl restart nginx


echo "[+] Installing DoH-client for transparent UDP to DoH conversion"
# Install GO
curl -OL https://golang.org/dl/go1.16.7.linux-amd64.tar.gz
sudo tar -C /usr/local -xvf go1.16.7.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
mkdir ~/gopath
export GOPATH=~/gopath

# Install dns-over-https server
git clone https://github.com/m13253/dns-over-https.git
cd dns-over-https/
make
sudo make install

# Confiugure dns-over-https server
cat << EOF > /etc/dns-over-https/doh-server.conf
listen = [
    "127.0.0.1:8053",
    "[::1]:8053",
]

local_addr = ""
cert = ""
key = ""
path = "/dns-query"

upstream = [
    "udp:192.168.0.20:53",
]

timeout = 10
tries = 3
verbose = true
log_guessed_client_ip = false
ecs_allow_non_global_ip = false
ecs_use_precise_ip = false
EOF

# Enable/disable, start/stop systemd services
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
sudo systemctl start doh-server.service
sudo systemctl enable doh-server.service
systemctl daemon-reload