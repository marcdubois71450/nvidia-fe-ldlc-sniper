# Description

NVIDIA 3090 3080 3070 3060Ti FE LDLC Sniper

Old version : https://pastebin.com/raw/HMNDCiKd https://pastebin.com/raw/Kyh5Vg3L

If you update the search on ldlc too often your IP address will be banned, that's why this bot is linked to a twitter account.

# Run bot

Installation of necessary tools
```
apt -y update
apt install git python3-pip screen unzip curl unzip xvfb libxi6 libgconf-2-4 default-jdk -y
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
pip3 install tweepy selenium requests webdriver-manager lxml
```
We configure ldlc account, card information and tweet api acces token. For that we will use the `nano` text editor :
```
nano main.py
```
You should see this
```
LDLC_ACCOUNT = {
    'email' : 'user@domain.tld',
    'password': 'amazingpassword'
}

CARD = {
    'num' : 'XXXXXXXXXXXXXXXXXX',
    'date': 'XX/XX',
    'secret': 'XXX',
    'name': 'Xxxxxx Xxxxxxxxxx'
}

# Twitter
consumer_key = 'x'
consumer_secret = 'x'
access_token = 'x'
access_token_secret = 'x'
```
Replace its information with your information

You can now save the file with `CTRL + O` then `Enter`. And quit `nano` text editor with `CTRL + X`


You can now start your bot
```
python3 main.py
```

- Cron (Auto restart on reboot)
```
crontab -e
```
Add this below the comment :
```
@reboot cd /root/nvidia-fe-ldlc-sniper/ && /usr/bin/python3 main.py
```

- Check all log
```
cat /var/log/nvidia-sniper.log
```

- Check live log
```
tail -f /var/log/nvidia-sniper.log
```
