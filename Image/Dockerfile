#Use an existing docker image as a base
FROM ubuntu

#Installing Anaconda on Ubuntu Image
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y sudo
RUN apt-get install -y wget
RUN apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 -y
RUN wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
RUN yes "yes" | bash /tmp/Anaconda3-2020.02-Linux-x86_64.sh
RUN apt-get install locate
ENV PATH /yes/bin:$PATH

#Updating Anaconda
RUN conda init

#Updating Anaconda
RUN conda update --all -y