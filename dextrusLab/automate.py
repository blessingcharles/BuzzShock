import sys
import docker


# actix=8001
# gunicorn=8002
# nodejs=8003
# golang=8004
# java=8005
# hyper=8006

servers_container = {
    "actix-server":8001 ,
    "gunicorn-server":8002 ,
    "nodejs-server":8003 ,
    "golang-server":8004 ,
    "java-server":8005 ,
    "hyper-server":8006
}

proxies_container = {
    "caddy-proxy":9001 ,
    "nginx-proxy":9002 ,
    "haproxy-proxy":9003 ,
    "httpd-proxy":9004 ,
    "traefik-proxy":9005 ,
    "apacheTraffic-proxy":9006
}
# caddy=9001
# nginx=9002
# haproxy=9003
# httpd=9004
# traefik=9005
# apacheTraffic=9006

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("./tool <start/stop>")
        exit(0)


    client = docker.from_env()

    if sys.argv[1] == 'start':
        for container_name , port in servers_container.items():
            print("Starting : " , container_name , " port: " , str(port))
            client.containers.run(container_name ,ports={ '80/tcp':port } , name=container_name )

    if sys.argv[1] == "stop":
        containers_list = client.containers.list()
        for container in containers_list:
            container.stop()
