FROM jodafons/root

LABEL maintainer "Joao Victor da Fonseca Pinto <jodafons@lps.ufrj.br>"

USER root
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen

# Install Gaugi
RUN pip install tensorflow==2.0.0b1
RUN pip install gaugi saphyra future numpy onnxruntime


# Install Latex
RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended xzdec -y \
    && rm -rf /var/lib/apt/lists/*

RUN ls -lisah
RUN mkdir /code && cd /code && git clone https://github.com/jodafons/prometheus.git && cd prometheus && mkdir build \
    && cd build && cmake .. && make

COPY setup_envs.sh /

RUN mkdir /ci
COPY sample.root /ci
COPY parser.py /parser.py
ENTRYPOINT ["/parser.py"]


