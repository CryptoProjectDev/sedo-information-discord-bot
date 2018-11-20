# SEDO-information-discord-price-bot

![SEDO_small](http://sedocoin.org/wp-content/uploads/2018/10/logo_blue_240.png)

Bot to monitor/post price etc to the SEDO discord server

Forked from the https://github.com/0x1d00ffff/0xbtc-discord-price-bot

***************
2018-11-21
- added yobit price support
***************

Installation:

! REQUEIRED python 3.6.x. Dont worked in python 3.7.x

 - Clone this repository
 - Install python 3.6+
   - For debian 9 users: Debian 9 repositories only go up to python 3.5, so to
     install the latest 3.6.x python version:
     - install prerequisites:

         sudo apt install build-essential checkinstall libreadline-gplv2-dev \
         libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
         libbz2-dev libffi-dev

     - `https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz`
     - `tar xvf Python-3.6.7.tgz`
     - `cd Python-3.6.7/`
     - `./configure --enable-optimizations --with-ensurepip=install`
     - `make -j2` (or `make -j8` if you have a cpu with lots of threads)
     - `sudo make altinstall`
 - run `pip3 install -r requirements.txt`
   - For for Windows Users: This command failed for me with error:
   `error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\BIN\\link.exe' failed with exit status 1158`
   - The fix: Copy rc.exe and rcdll.dll from `C:\Program Files (x86)\Windows Kits\8.1\bin\x86` to `C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin`
 - copy `template_secret_info.py` to `secret_info.py` and fill in your bot's authentication settings
 - edit `configuration.py` (you can run the bot with `--show_channels` to get channel IDs)
 - (Optional) edit `apis` list at the end of `main.py`
 - run `python3 /path/to/price-bot/`


Requires:
 - python3
 - websocket
 - discord
 - web3.py
 - BeautifulSoup (only if !holders command is enabled)
 - matplotlib (only if !holders command is enabled)

Bugs:
 - `!mine test` fails since it expects a checksum address
 - occasionally APIs return NaN as a data point.. which is a valid float. Need
   to explicitly check for this.
 - `--command_test` bypasses command preprocessing (.lower().strip()) etc
 - if a command string matches two commands it will run both and return
   the response from whatever command runs last.

