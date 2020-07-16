FROM jodafons/root

LABEL maintainer "Joao Victor da Fonseca Pinto <jodafons@lps.ufrj.br>"

USER root
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen

# Install Gaugi
RUN pip install gaugi saphyra future numpy




ARG ONNXRUNTIME_REPO=https://github.com/Microsoft/onnxruntime
ARG ONNXRUNTIME_SERVER_BRANCH=v1.3.1

RUN apt-get update &&\
    apt-get install -y sudo git bash


# Prepare onnxruntime repository & build onnxruntime
RUN cd /opt && git clone --single-branch --branch ${ONNXRUNTIME_SERVER_BRANCH} --recursive ${ONNXRUNTIME_REPO} onnxruntime &&\
    /bin/sh onnxruntime/dockerfiles/scripts/install_common_deps.sh &&\
    cd onnxruntime &&\
    /bin/sh ./build.sh --config Release --build_wheel --update --build --parallel --cmake_extra_defines ONNXRUNTIME_VERSION=$(cat ./VERSION_NUMBER) &&\
    pip install /opt/onnxruntime/build/Linux/Release/dist/*.whl





# Install Latex
RUN apt-get install -y zsh
RUN sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended xzdec -y \
    && rm -rf /var/lib/apt/lists/*


RUN pip install tensorflow==2.0.0b1


COPY setup_envs.sh /
RUN chmod 777 /setup_envs.sh
