FROM jodafons/root

LABEL maintainer "Joao Victor da Fonseca Pinto <jodafons@lps.ufrj.br>"

USER root
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen


RUN ls
# Install Gaugi
RUN pip install --upgrade gaugi saphyra future numpy onnxruntime

# Make images Grid / Singularity compatible
#RUN mkdir -p /alrb /cvmfs /afs /eos /data



# Install Latex
RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended xzdec -y \
    && rm -rf /var/lib/apt/lists/*

<<<<<<< HEAD:docker/local/Dockerfile
=======

>>>>>>> 9a978f3b9db3ef4340a5c60965e116d4869800b0:docker/local/Dockerfile


COPY setup_envs.sh /
RUN chmod 777 /setup_envs.sh


