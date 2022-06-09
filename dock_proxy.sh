echo -en "Starting Proxy"

sudo docker run -dp 9001:80 caddy-proxy

sudo docker run -dp 9002:80 nginx-proxy

sudo docker run -dp 9003:80 haproxy-proxy

sudo docker run -dp 9004:80 httpd-proxy

sudo docker run -dp 9005:80 traefik-proxy