FROM ubuntu:18.04

LABEL maintainer "Joao Victor da Fonseca Pinto <jodafons@lps.ufrj.br>"

ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen
RUN mkdir /eos
RUN mkdir /afs
USER root
SHELL [ "/bin/bash", "-c" ]
#RUN rm /bin/sh && ln -s /bin/bash /bin/sh





RUN apt-get update --fix-missing
RUN apt-get install -y python3.7 python3-pip
RUN apt-get install -y git \
                       wget \
                       dpkg-dev \
                       g++ \
                       gcc \
                       binutils \
                       libx11-dev \
                       libxpm-dev \
                       libxft-dev \
                       libxext-dev \
                       gfortran \
                       libssl-dev \
                       libpcre3-dev \
                       libglew1.5-dev \
                       libftgl-dev \
                       libldap2-dev \
                       python-dev \
                       libxml2-dev \
                       libkrb5-dev \
                       libgsl0-dev \
                       libqt4-dev \
                       libfftw3-dev \
                       libcfitsio-dev \
                       graphviz-dev \
                       libavahi-compat-libdnssd-dev \
                       libboost-all-dev \
                       vim \
                       qt4-default \
                       librange-v3-dev \
                       libboost-python-dev


RUN git clone https://github.com/amix/vimrc.git ${HOME}/.vim_runtime
RUN cd ${HOME}/.vim_runtime/ && source install_awesome_vimrc.sh 
RUN wget https://cmake.org/files/v3.17/cmake-3.17.2-Linux-x86_64.sh -P /usr/
RUN chmod 755 /usr/cmake-3.17.2-Linux-x86_64.sh
RUN cd /usr && ./cmake-3.17.2-Linux-x86_64.sh --skip-license
RUN ln -sf /usr/bin/python3.6 /usr/bin/python



# Install ROOT
RUN CPU_N=$(grep -c ^processor /proc/cpuinfo) && cd /opt && git clone https://github.com/root-project/root.git && \
cd root && git checkout v6-16-00 && mkdir buildthis && cd buildthis && cmake  --Dpython_version=3 .. && make -j$CPU_N
ENV ROOTSYS "/opt/root/buildthis/"
ENV PATH "$ROOTSYS/bin:$PATH"
ENV LD_LIBRARY_PATH "$ROOTSYS/lib:$LD_LIBRARY_PATH"
ENV PYTHONPATH "/opt/root_cern/build/lib:$PYTHONPATH"


RUN ln -sf /usr/bin/pip3 /usr/bin/pip

COPY setup_envs.sh /
RUN chmod 777 /setup_envs.sh
