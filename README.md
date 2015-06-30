# IPOP-client
Client UI for IPOP

###External dependencies:
- pyqt4
- pycrypto
- sleekxmpp
- gksudo

###Current features:
- Monitoring network statistics
- Secure connection to server

###Installation instructions:
Install all the required packages with the following command

```
sudo apt-get install python-qt4 python-pip pyqt4-dev-tools gksu
sudo pip install sleekxmpp
```

clone this repo

```
git clone https://github.com/HotSushi/IPOP-client.git
cd IPOP-client
```

convert views into class

```
pyuic4 ui/login.ui > ui/login.py
pyuic4 ui/monitor.ui > ui/monitor.py
```


