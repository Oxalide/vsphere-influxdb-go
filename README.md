[![Go Report Card](https://goreportcard.com/badge/Oxalide/vsphere-influxdb-go)](https://goreportcard.com/report/github.com/Oxalide/vsphere-influxdb-go)

# Collect VMware vSphere, vCenter and ESXi performance metrics and send them to InfluxDB

# External dependencies

* [govmomi](https://github.com/vmware/govmomi)
* [influxDB go client](https://github.com/influxdata/influxdb/tree/master/client/v2)

You'll need to go get them both for the script to work:
```
go get github.com/vmware/govmomi
go get github.com/influxdata/influxdb/client/v2

```

# Run


```

go get github.com/oxalide/vsphere-influxdb-go

```
This will install the project in your $GOBIN($GOPATH/bin). If you have appended $GOBIN to your $PATH, you will be able to call it directly. Otherwise, you'll have to call it with its full path. 
Example:
```
vsphere-influxdb-go
```
or :
```
$GOBIN/vsphere-influxdb-go
```


# Configure

You'll need a JSON file with all your vCenters/ESXi to connect to, the InfluxDB connection details(url, username/password, database to use), and the metrics to collect.

If you set a domain, it will be automaticaly removed from the names of the found objects.

Metrics collected are defined by associating ObjectType groups with Metric groups.
To see all available metrics, check out [this](http://www.virten.net/2015/05/vsphere-6-0-performance-counter-description/) page. 

Note: Not all metrics are available directly, you might need to change your metric collection level. 
A table with the level needed for each metric is availble [here](http://www.virten.net/2015/05/which-performance-counters-are-available-in-each-statistic-level/), and you can find a PowerCLI script that changes the collect level [here](http://www.valcolabs.com/2012/02/06/modify-historical-statistics-level-using-powercli/)

An example of configuration file is [here](./vsphere-influxdb.json.sample).

You need to place it at /etc/*binaryname*.json (/etc/vsphere-influxdb.json by default) or you can specify a different location using the config flag.


# Run as a service

Create a crontab to run it every X minutes(one minute is fine - in our case, ~30 vCenters, ~100 ESXi and ~1400 VMs take approximately 25s to collect all metrics - rather impressive, i might add).
```
* * * * * $HOME/work/go/bin/vsphere-influxdb-go
```


# TODO
* Add service discovery(or probably something like [Viper](https://github.com/spf13/viper) for easier and more flexible configuration with multiple backends)
* Add extra tags(cluster for the hosts, etc.)

# Contributing
You are welcome to contribute!

# License 

The original project, upon which this one is based, is written by cblomart, sends the data to Graphite, and is available [here](https://github.com/cblomart/vsphere-graphite). 

This one is licensed under GPLv3. You can find a copy of the license in [LICENSE.txt](./LICENSE.txt)


