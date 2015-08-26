run 
sudo apt-get install -y ganglia-monitor

copy 
conf.d/ --> /etc/ganglia
gmond.conf --> /etc/ganglia

open /usr/lib/ganglia
mkdir python_modules
copy ipop_ganglia.py --> python_modules

change /usr/lib/ganglia/python_modules/ipop_ganglia.py:22 to point to the stats folder.
