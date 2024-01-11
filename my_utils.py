import pandas as pd
import numpy as np
import os
import config
import matplotlib.pyplot as plt
from chat_downloader import ChatDownloader
from scipy.signal import find_peaks


url = 'https://www.youtube.com/watch?v=jfKfPfyJRdk' 
url = 'https://www.youtube.com/watch?v=YspBTHE-55I' # 1:32:00
# url = 'https://www.youtube.com/watch?v=6J6QqtHKAlw' # 6:xx:xx


def get_chat(url):
    chat = ChatDownloader().get_chat(url)       # create a generator

    id=chat.id
    print(f"using file: {id}")

    if not os.path.isfile(f"raw_csv/{id}.csv"):
        chat = ChatDownloader().get_chat(url, output=f"raw_csv/{id}.csv") 
        for message in chat:                        # iterate over messages
            chat.print_formatted(message)     

    if not os.path.isfile(f"csv/{id}.csv"):
        df=pd.read_csv(f"raw_csv/{id}.csv", usecols=config.FILTER_CSV)
        df.to_csv(f"csv/{id}.csv")
    return id
        

def get_peaks(id):
    full = pd.read_csv(f"csv/{id}.csv")
    # slim = pd.read_csv(f"csv/{id}.csv", usecols=['timestamp'])

    time0=int(full['time_in_seconds'].iloc[0])
    print(f"zero time: {time0}")

    ts = full['time_in_seconds'].to_numpy()
    ts = ts.astype(int) - time0         #rendo 0 index


    print(ts)
    range_ts = ts[-1]-ts[0]

    timeline=np.arange(ts[0], ts[-1]+1, dtype=float)

    #duplico e metto a zero il secondo
    timeline = np.repeat(timeline, 2).reshape((range_ts+1,2))    
    timeline_density = timeline.copy()   
    timeline[:,1]=0

    print(timeline)

    for t in ts:
        timeline[t][1]+=1

    timeline[:,0] = timeline[:,0]  + time0
    timeline_density[:,0] = timeline_density[:,0]  + time0
    print(timeline)

    win_size=60      #secondi della finestra
    window = np.ones((1,win_size))
    window=window[0]*(1/win_size)

    density = np.convolve(timeline[:,1],window, mode='same')
    print("density: ", density)
    timeline_density[:,1] = density
    print("timeline density pre: ",timeline_density)
    print("density: ", density)
    print("timeline density after: ",timeline_density)
        
    avg = np.average(timeline_density[:,1])
    # peaks1, _ = find_peaks(density, distance=win_size*3)
    peaks2, _ = find_peaks(density, prominence=0.5)

    print(peaks2)
    print(timeline_density[peaks2[0], 0])

    plt.axhline(y = avg, color = 'r', linestyle = '-') 
    plt.plot(*zip(*timeline_density))
    plt.plot(peaks2+ time0, density[peaks2], "or")
    # plt.plot(peaks1+ time0, density[peaks1], "ob", color = 'g')
    if not os.path.isfile(f'img/{id}.png'):
        plt.savefig(f'img/{id}.png')    
    # plt.show()

    for i in peaks2:
        print(f"highlight {i+1} @ https://www.youtube.com/watch?v={id}&t={i+time0-win_size}s")

    return peaks2

def parse(url):
    id = get_chat(url)
    return id, get_peaks(id)
