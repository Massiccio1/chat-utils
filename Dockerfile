FROM python:alpine3.19

RUN pip install matplotlib 
RUN pip install pandas 
RUN pip install chat_downloader  
RUN pip install scipy
RUN pip install Flask
RUN pip install flask_cors
# RUN pip install request
# RUN pip install jsonify

RUN mkdir -p /app
WORKDIR /app
EXPOSE 8060
COPY . /app

CMD python3 api.py



#           docker build -t USESR/chat:latest .
#           docker run -p 8060:8060 USER/chat:latest

