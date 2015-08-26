#How To setup ganglia monitoring for client node

##Run 
```
sudo apt-get install -y ganglia-monitor
```

##Copy 
```
conf.d/ --> /etc/ganglia
gmond.conf --> /etc/ganglia
```
##Then
```
open /usr/lib/ganglia
mkdir python_modules
copy ipop_ganglia.py --> python_modules/
```

##Changes
change `/usr/lib/ganglia/python_modules/ipop_ganglia.py:22` to point to the stats folder.
