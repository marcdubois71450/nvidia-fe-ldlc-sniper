# Description

NVIDIA 3090 3080 3070 3060Ti FE LDLC Sniper

Old version : https://pastebin.com/raw/HMNDCiKd https://pastebin.com/raw/Kyh5Vg3L

If you update the search on ldlc too often your IP address will be banned, that's why this bot is linked to a twitter account.

# Start bot

```
git clone https://github.com/marcdubois71450/nvidia-fe-ldlc-sniper.git
cd nvidia-fe-ldlc-sniper
nano main.py  # Set your ldlc account, card information and tweet api accès token. For save in nano: CTRL+O, for quit: CTRL+X
pip3 install tweepy selenium requests webdriver-manager
python3 main.py
```

 - In Screen

```
apt install screen
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
