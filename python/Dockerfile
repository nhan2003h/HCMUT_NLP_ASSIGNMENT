# Written by: Hung Vo (thanhhungqb@gmail.com)
# 
# can be used by wide project of DL (demo)
#

# =====================================================================
# base-image maybe share for quicker build and save storage
# thanhhungqb/python-builder:ver
# =====================================================================

FROM python:3.8-slim-buster as python-builder

LABEL author = "Hung Vo" 
LABEL contact.gmail = "thanhhungqb@gmail.com"

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Ho_Chi_Minh

RUN apt-get update && apt-get install -y --no-install-recommends locales git wget apt-utils  && \
    apt -y --no-install-recommends install make cmake gcc g++ build-essential && \  
    apt -y --no-install-recommends install libsndfile1-dev ffmpeg && \  
    pip3 install --upgrade pip && \  
    locale-gen en_US.UTF-8  && \  
    rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \    
    locale-gen
    
ENV LANG en_US.UTF-8    
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


# =====================================================================
# builder stage, maybe from python-builder or thanhhungqb/python-builder:TAG (for quicker to build, remove above part when use pre-build image)
# install all libraries and dependency (both pip and apt if needed)
# after that, just copy needed file for small, clean runtime image bellow.
# in most of simple case, you are not need to modify this part, just provide requirements.txt and DONE.
# if provide setup instead requirements, use: pip3 install -e . after COPY command
# in some case, use apt install is needed, refer to python-builder to copy similar install command
# =====================================================================

FROM python-builder as builder

# use venv and copy to runtime
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# RUN apt-get update && apt-get install -y --no-install-recommends LIBRARIES HERE

COPY requirements.txt /src/requirements.txt
RUN python3 -m pip install --upgrade pip && \
	pip install -r /src/requirements.txt && \
    rm -rf /root/.cache/pip


# =====================================================================
# final part: build the runtime image
# keep it simple and clean
# =====================================================================

FROM python:3.8-slim-buster as runtime
LABEL author = "Hung Vo" 
LABEL contact.gmail = "thanhhungqb@gmail.com"

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Ho_Chi_Minh

# install neccessary apt libraries here
# use --no-install-recommends in most case
RUN apt-get update && apt-get -y --no-install-recommends install locales && \
	apt-get -y --no-install-recommends install ffmpeg && \
	locale-gen en_US.UTF-8 && \
	rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
	
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


# Make sure we use the virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /src/

EXPOSE 5000

WORKDIR /src/

CMD ["python3", "-m", "hcommon.cli", "run", "--json_conf", "conf/app.json"]
