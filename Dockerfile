FROM ubuntu:18.04
FROM python:3.9

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Change timezone
RUN echo "Europe/Paris" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# set work directory
WORKDIR /usr/src/app
ENV PYTHONPATH $PYTHONPATH:/src

# Add python dependcies
COPY requirements.txt requirements.txt

# Create venv and install dependencies
RUN python3.9 -m venv allisone
RUN chmod u+x allisone/bin/activate
RUN ./allisone/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copy project
COPY . /usr/src/app/

# Expose Webserver Http port
EXPOSE 5001

# Run server
RUN chmod u+x app.sh
CMD ./app.sh