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

download gvpn+ipop executable from here [minimal_gvpn.tar.gz](https://drive.google.com/file/d/0Bxr9CriT1DIuZ0lWRXZhd3hpbTA/view?usp=sharing)

Extract this to a directory, say `home/user/ipop`

Make another directory where ipop can dump ganglia stats into, say `home/user/ipopstats`

Do this step only if your system is 32 bit: Go into extracted `home/user/ipop` directory, open script.sh, and change `sudo ./ipop-tincan-x86_64 1> out.log 2> err.log &` to `sudo ./ipop-tincan-x86 1> out.log 2> err.log &`

Move to `IPOP-client` directory and edit `config.json` file to reflect where ipop executable is and ganglia stats destination is
`IPOP-client/config.json`
```
{
"ganglia_path":"/home/user/ipopstats",
"working_path":"/home/user/ipop"
}
```



