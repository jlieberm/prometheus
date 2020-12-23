FROM ringeratlas/ringer

LABEL maintainer "Joao Victor da Fonseca Pinto <jodafons@lps.ufrj.br>"

USER root
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen

COPY setup_prometheus.sh /
RUN chmod 777 /setup_prometheus.sh


