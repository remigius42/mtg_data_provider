FROM python:3.6

LABEL maintainer="andreas.remigius@gmail.com" \
      version=0.1 \
      description="Data gatherer and preprocessor for 'Magic the Gathering' \
cards. By default fetches card data in 'deck.yml' and stores the images \
along with the generated variations in the sub directory 'data' relative \
to the current directory expected to be mounted as '/mnt/mtg'. \
The expected invocation syntax is:\
'docker run -v $(pwd):/mnt/mtg [deck.yml] [data]'

COPY ["pip-requirements.txt", "/tmp/pip-requirements.txt"]
RUN ["pip","install","-r","/tmp/pip-requirements.txt"]

WORKDIR /mnt/mtg
ENTRYPOINT ["python", "main.py"]
CMD ["-d", "deck.yml", "-o", "data"]
