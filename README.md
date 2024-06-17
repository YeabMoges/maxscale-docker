# MariaDB MaxScale Docker image

## Introduction

This setup provides a simple and efficient way to deploy MariaDB MaxScale along with two MariaDB master servers using Docker Compose.
This Docker image runs the latest 2.4 version of MariaDB MaxScale. 
[The MaxScale docker-compose setup](./docker-compose.yml) contains MaxScale
configured with a master container and a maxscale container.


The initial fork was taken from [Zohan repository](https://github.com/Zohan/maxscale-docker), which followed a 1 master and 2 slaves cluster setup. 

## Running

Clone the repository

```
git clone https://github.com/YeabMoges/maxscale-docker
cd maxscale-docker/maxscale
```

To start, run the
following commands in this directory.

```
docker-compose up -d
```

Verify

```
sudo docker-compose up -d
```

To run maxctrl in the container to see the status of the cluster:
```
$ sudo docker-compose exec maxscale maxctrl list servers
```

The result should look something like this
```
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬──────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID     │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ master1 │ master1 │ 3306 │ 0           │ Master, Running │          │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ replica │ replica │ 3306 │ 0           │ Running         │          │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴──────────┘
```
After MaxScale and the servers have started (takes a few minutes), you can find
the readwritesplit router on port 4006 and the readconnroute on port 4008. The
user `maxuser` with the password `maxpwd` can be used to test the cluster.
Assuming the mariadb client is installed on the host machine:
```
$ mysql -umaxuser -pmaxpwd -h 127.0.0.1 -P 4006 test
```
```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 10.2.12 2.2.9-maxscale mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [test]>
```

## Configuration
### MariaDB Servers
Two MariaDB master servers are configured to run with Docker, each initialized with a server ID and configuration directory:

- master1:
    - Port: 4001
    - Server ID: 3000
    - Configuration: /sql/master1

- replica:
    - Port: 4002
    - Server ID: 3001
    - Configuration: /sql/master2

### Maxscale
MaxScale is configured with the following section in [example.cnf](./maxscale-docker/maxscale/maxscale.cnf.d/example.cnf):

```
[server1]
type=server
address=master1
port=3306
protocol=MariaDBBackend

[server2]
type=server
address=master2
port=3306
protocol=MariaDBBackend
```

### Sharded 
configured with the following section in [example.cnf](./maxscale-docker/maxscale/maxscale.cnf.d/example.cnf):





















