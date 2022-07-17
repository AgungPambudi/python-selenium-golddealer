# python-selenium-golddealer

How to install package dependencies headless Chrome on Ubuntu Server

$ sudo apt-get update
$ sudo apt-get install -y libappindicator1 fonts-liberation
$ sudo apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable
$ cd /temp
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome*.deb
$ sudo ps aux | grep chrome

