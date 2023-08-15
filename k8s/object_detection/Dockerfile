#Base image #3.5GB 
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu18.04

# Update apt packages #54MB
RUN apt update
RUN apt upgrade -y

# Install vim #55MB 
RUN apt install vim -y

# Install python 3.7 # 88MB
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.7 -y

#installing dependencies for pillow #28 MB
RUN apt install -y zlib1g-dev libjpeg-dev libpng-dev 

# Make python 3.7 the default
RUN echo "alias python=python3.7" >> ~/.bashrc
RUN export PATH=${PATH}:/usr/bin/python3.7
RUN /bin/bash -c "source ~/.bashrc"

# Add 3.7 to the available alternatives
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# Set python3.7 as the default python
RUN update-alternatives --set python3 /usr/bin/python3.7

# Install pip #280 MB
RUN apt install python3-pip -y
RUN python3 -m pip install --upgrade pip

#check python version
RUN python3 --version  

#create data directory to mount bind 
RUN mkdir /data/
RUN mkdir -p /home/compass/pycompass

#designate work directory 
WORKDIR /home/compass/pycompass  

#expose port in container. run this and then push to remote server  
EXPOSE 3000

#copy and install requirementsB
COPY requirements.txt . 
RUN pip3 install -r requirements.txt
RUN pip3 install fastapi 
RUN pip3 install uvicorn 

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install opencv-python
RUN pip3 install Pillow

RUN pip3 install climage 
RUN pip3 install cvlib
RUN pip3 install python-multipart 
COPY model_main.py .
EXPOSE 8000  
#execute command 
CMD ["python3", "model_main.py"]
