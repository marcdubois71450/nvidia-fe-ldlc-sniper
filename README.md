# Description

NVIDIA 3090 3080 3070 3060Ti FE LDLC Sniper

Old version : https://pastebin.com/raw/HMNDCiKd https://pastebin.com/raw/Kyh5Vg3L

If you update the search on ldlc too often your IP address will be banned, that's why this bot is linked to a twitter account.

# Start bot

```
apt -y update
apt install git python3-pip screen chromium unzip curl unzip xvfb libxi6 libgconf-2-4 default-jdk -y
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt -y update
apt -y install google-chrome-stable
wget https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
git clone https://github.com/marcdubois71450/nvidia-fe-ldlc-sniper.git
cd nvidia-fe-ldlc-sniper
nano main.py  # Set your ldlc account, card information and tweet api accès token. For save in nano: CTRL+O, for quit: CTRL+X
pip3 install tweepy selenium requests webdriver-manager lxml
python3 main.py
```

 - In Screen

```
screen -S ldlcbot

cd nvidia-fe-ldlc-sniper
python3 main.py >> /var/log/ldlcbot.log
```
For quit screen ``CTRL+A`` and ``CTRL+D``


- Check all log
```
cat /var/log/ldlcbot.log
```

- Check live log
```
tail -f /var/log/ldlcbot.log
```

 - Re-enter in screen
```
screen -r ldlcbot
```
