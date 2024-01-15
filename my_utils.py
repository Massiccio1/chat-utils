import pandas as pd
import numpy as np
import os   
import config
import matplotlib.pyplot as plt
from chat_downloader import ChatDownloader
from scipy.signal import find_peaks
from tempfile import TemporaryFile
import time
import re
import datetime
import json


url = 'https://www.youtube.com/watch?v=jfKfPfyJRdk' 
url = 'https://www.youtube.com/watch?v=YspBTHE-55I' # 1:32:00
# url = 'https://www.youtube.com/watch?v=6J6QqtHKAlw' # 6:xx:xx

def int_to_ts(sec):
    return time.strftime('%H:%M:%S', sec)


def get_chat(url):
    chat = ChatDownloader().get_chat(url)       # create a generator

    id=chat.id
    title = chat.title
    print(f"using file: {id}")
    # print(os. getcwd())
    if not os.path.isfile(f"raw_csv/{id}.csv"):
        chat = ChatDownloader().get_chat(url, output=f"raw_csv/{id}.csv") 
        for message in chat:                        # iterate over messages
            chat.print_formatted(message)     

    if not os.path.isfile(f"csv/{id}.csv"):
        
        df=pd.read_csv(f"raw_csv/{id}.csv", usecols=config.FILTER_CSV)
        df.to_csv(f"csv/{id}.csv")
    
    if not os.path.isfile(f"chat/{id}.html"):
        build_html(id, title)
        
    if not os.path.isfile(f"info/{id}.json"):
        build_info(chat)
    
    return id, title

def save_data(id, range, data):
    # print("saving....")
    # if os.path.isfile(f'data/{id}.npy'):
    #     os.remove(f'data/{id}.npy')
    with open(f'data/{id}-{range}.npy', 'wb') as f:
        np.save(f, data)
        
def load_data(id,range):
    # print("loading....")
    data = np.empty((1,1))
    with open(f'data/{id}-{range}.npy', 'rb') as f:
        data = np.load(f)
    return data

def build_info(chat):
    tn=f"https://img.youtube.com/vi/{chat.id}/mqdefault.jpg"
    info = {
        "id":chat.id,
        "title":chat.title,
        "thumbnail":tn,
        "timestamp":chat.start_time//1000000,
        "datetime":datetime.datetime.fromtimestamp(int(chat.start_time)/1000000).strftime("%d/%m/%Y, %H:%M:%S"),
        "duration":chat.duration
    }
    with open(f"info/{chat.id}.json", 'w') as outfile:
        json.dump(info, outfile)
        
def build_html(id, title, filter="", save=True):
    
    print("building html table")
    full = pd.read_csv(f"csv/{id}.csv")
    head = f"<h2>{title}</h2><br><table>"
    tail = "</table>"
    table = ""+head
    """
    <table>
        <tr>
            <th>Company</th>
            <th>Contact</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>Alfreds Futterkiste</td>
            <td>Maria Anders</td>
            <td>Germany</td>
        </tr>
        <tr>
            <td>Centro comercial Moctezuma</td>
            <td>Francisco Chang</td>
            <td>Mexico</td>
        </tr>
    </table>
    """       
    pattern = re.compile(filter, re.IGNORECASE)
    for index, message in full.iterrows():
        
        if filter!="":
            match = pattern.search(message.message)
            # Check if a match is found
            if not match:
               continue
                
        sec = message.time_in_seconds
        if sec < 0:
            sec = 0
        text = f'<tr><td>{time.strftime("%H:%M:%S", time.gmtime(sec))}</td><td>{message["author.name"]}</td><td>{message.message}</td></tr>\n'
        table = table + text
    table=table+tail
    
    if save:
        with open(f"chat/{id}.html", "w") as text_file:
            text_file.write(table)
        print("done with html")
        return 0
    else:
        return table

def get_peaks(id, prominence=0.5, range=60):
    timeline_density=np.empty((1,1))
    if not os.path.isfile(f"data/{id}-{range}.csv"):    #numpy non salvato
        full = pd.read_csv(f"csv/{id}.csv")
        # slim = pd.read_csv(f"csv/{id}.csv", usecols=['timestamp'])
        time0=int(full['time_in_seconds'].iloc[0])
        # print(f"zero time: {time0}")

        ts = full['time_in_seconds'].to_numpy()
        ts = ts.astype(int) - time0         #rendo 0 index


        # print(ts)
        range_ts = ts[-1]-ts[0]

        timeline=np.arange(ts[0], ts[-1]+1, dtype=float)

        #duplico e metto a zero il secondo
        timeline = np.repeat(timeline, 2).reshape((range_ts+1,2))    
        timeline_density = timeline.copy()   
        timeline[:,1]=0

        # print(timeline)

        for t in ts:
            timeline[t][1]+=1

        timeline[:,0] = timeline[:,0]  + time0
        timeline_density[:,0] = timeline_density[:,0]  + time0
        # print(timeline)

        win_size=range      #secondi della finestra
        window = np.ones((1,win_size))
        window=window[0]*(1/win_size)

        density = np.convolve(timeline[:,1],window, mode='same')
        # print("density: ", density)
        timeline_density[:,1] = density
        save_data(id,range,timeline_density)
    else:
        timeline_density=load_data(id,range)
    # print("timeline density pre: ",timeline_density)
    # print("density: ", density)
    # print("timeline density after: ",timeline_density)
        
    avg = np.average(timeline_density[:,1])
    # print(timeline_density)
    # peaks1, _ = find_peaks(density, distance=win_size*3)
    peaks2, _ = find_peaks(timeline_density[:,1], prominence=prominence)

    # print(peaks2)
    # print(timeline_density[peaks2[0], 0])
    
    # peaks2 = peaks2[(avg > peaks2) | (peaks2 >avg)]
    
    peaks3=np.array([],dtype=int)
    # print("avg: ", avg)
    # print("shape: ", timeline_density.shape)
    # print("peaks2:", peaks2)
    
    for p in peaks2:        #filter spikes lower that avg
        
        lower = max(0, p-range//2)
        upper = min(timeline_density.shape[0]-1 , p+range//2)
        
        # print("bounds => ", lower, ":", upper)
        
        index = np.argmax(timeline_density[lower:upper,1])
        val = timeline_density[lower+index,1]
        # print("inde of max: ", index)
        # print("max val in range: ",val)
        if val>avg:
            peaks3=np.append(peaks3,index+lower)
    
    # if True:
    #     last=0
    #     for i in range(peaks3.size):
        
    
    # print(peaks2)
    # print(peaks3)
            
    plt.grid()
    plt.axhline(y = avg, color = 'r', linestyle = '-') 
    plt.plot(*zip(*timeline_density))
    plt.plot(peaks3+ time0, timeline_density[:,1][peaks3], "or")
    # plt.plot(peaks1+ time0, density[peaks1], "ob", color = 'g')
    if os.path.isfile(f'img/{id}-{range}.png'):
        os.remove(f'img/{id}-{range}.png')
    plt.savefig(f'img/{id}-{range}.png')
    plt.close()
    # plt.show()

    # for i in peaks3:
    #     print(f"highlight {i+1} @ https://www.youtube.com/watch?v={id}&t={i+time0-win_size}s")
    
    
    # print("peaks value: ", timeline_density[peaks3,1])
    # print("ordered peaks: ", np.flip(np.sort(timeline_density[peaks3,0])))
    peaks3=np.unique(peaks3)
    ind = np.argsort(timeline_density[peaks3,1])
    peaks4=np.flip(peaks3[ind])
    
    # print("peaks value: ", timeline_density[peaks4,:])
    # print("ordered peaks: ", np.flip(np.sort(timeline_density[peaks4,1])))

    return peaks4

def parse(url, prominence=0.5, range=60):
    id, title = get_chat(url)
    peaks=get_peaks(id, prominence, range)
    
    return id, peaks.tolist() , title

if __name__=="__main__":
    a,b = parse(url)