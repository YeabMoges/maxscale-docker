# MariaDB MaxScale Docker image

## Introduction

This setup provides a simple and efficient way to deploy MariaDB MaxScale along with two MariaDB master servers using Docker Compose.
This Docker image runs the latest 2.4 version of MariaDB MaxScale. 
[The MaxScale docker-compose setup](./docker-compose.yml) contains MaxScale
configured with a master container and a maxscale container.

-	[Travis CI:  
	![build status badge](https://img.shields.io/travis/mariadb-corporation/maxscale-docker/master.svg)](https://travis-ci.org/mariadb-corporation/maxscale-docker/branches)
-       The initial fork was taken from [Zohan repository](https://github.com/Zohan/maxscale-docker), which followed a 1 master and 2 slaves cluster setup. 

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
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬──────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID     │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ master1 │ master1 │ 3306 │ 0           │ Master, Running │          │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ replica │ replica │ 3306 │ 0           │ Running         │          │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴──────────┘

After MaxScale and the servers have started (takes a few minutes), you can find
the readwritesplit router on port 4006 and the readconnroute on port 4008. The
user `maxuser` with the password `maxpwd` can be used to test the cluster.
Assuming the mariadb client is installed on the host machine:
```
$ mysql -umaxuser -pmaxpwd -h 127.0.0.1 -P 4006 test
```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 10.2.12 2.2.9-maxscale mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [test]>
```
You can edit the [`maxscale.cnf.d/example.cnf`](./maxscale.cnf.d/example.cnf)
file and recreate the MaxScale container to change the configuration.

To stop the containers, execute the following command. Optionally, use the -v
flag to also remove the volumes.

To run maxctrl in the container to see the status of the cluster:
```
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬──────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID     │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ server1 │ master  │ 3306 │ 0           │ Master, Running │ 0-3000-5 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Slave, Running  │ 0-3000-5 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Running         │ 0-3000-5 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴──────────┘

```

The cluster is configured to utilize automatic failover. To illustrate this you can stop the master
container and watch for maxscale to failover to one of the original slaves and then show it rejoining
after recovery:
```
$ docker-compose stop master
Stopping maxscaledocker_master_1 ... done
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬─────────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID        │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server1 │ master  │ 3306 │ 0           │ Down            │ 0-3000-5    │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Master, Running │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴─────────────┘
$ docker-compose start master
Starting master ... done
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬─────────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID        │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server1 │ master  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Master, Running │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴─────────────┘

```

Once complete, to remove the cluster and maxscale containers:

```
docker-compose down -v
```
