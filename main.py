import pandas as pd
import numpy as np
import os
import config
from chat_downloader import ChatDownloader

url = 'https://www.youtube.com/watch?v=jfKfPfyJRdk' 
url = 'https://www.youtube.com/watch?v=YspBTHE-55I'

chat = ChatDownloader().get_chat(url)       # create a generator

id=chat.id
chat = ChatDownloader().get_chat(url, output=f"raw_csv/{id}.csv") 

if not os.path.isfile(f"raw_csv/{id}.csv"):
    for message in chat:                        # iterate over messages
        chat.print_formatted(message)     

df=pd.read_csv(f"raw_csv/{id}.csv", usecols=config.FILTER_CSV)
df.to_csv(f"csv/{id}.csv")

