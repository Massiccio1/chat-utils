## Chat-utils

Barebone interface to automatically analyze youtube live chat

Based on the concentration of messages finds highlits moments

# How to run
Bare metal
```
git clone https://github.com/Massiccio1/chat-utils.git
cd chat-utils
bash requirements.txt
python3 api.py
```
Docker essential
```
git clone https://github.com/Massiccio1/chat-utils.git
cd chat-utils
docker build -t chat-utils .
docker run -d -p 8060:8060 chat-utils
```
Docker compose with mounted folders

```
git clone https://github.com/Massiccio1/chat-utils.git
cd chat-utils
docker build -t chat-utils .
docker compose up -d
```

and go to http://127.0.0.1:8060/index

There are 3 visual interfaces:

- `/index` - starting page to run the script
- `/chat` to view and filter already analyzed lives
- `/info` to display all the analyzed lives

And 1 useful API endpoint:
- `/parse` - POST with body
```

```