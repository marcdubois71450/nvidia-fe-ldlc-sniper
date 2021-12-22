# Description

NVIDIA 3090 3080 3070 3060Ti LDLC Sniper

Old version : https://pastebin.com/raw/HMNDCiKd https://pastebin.com/raw/Kyh5Vg3L

# Start bot

First edit main.py

```
git clone https://github.com/marcdubois71450/nvidia-fe-ldlc-sniper.git
cd nvidia-fe-ldlc-sniper
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
For quit screen CTRL+A and CTRL+D


- Check log all log
```
cat /var/log/ldlcbot.log
```

- Check log live log
```
tail -f /var/log/ldlcbot.log
```

 - Re-enter in screen
```
screen -r ldlcbot
```
