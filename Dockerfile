FROM python:3
MAINTAINER Tobias Bichlmaier


RUN pip --no-cache-dir install --upgrade pip
RUN git clone https://github.com/toebsen/python-denonavr
RUN pip install --no-cache-dir -r python-denonavr/requirements.txt
WORKDIR /python-denonavr

RUN python setup.py install

CMD ["denonavr_server", "-p", "5567"]
EXPOSE 5567

# docker build --rm -f "Dockerfile" -t python-denonavr:latest .
# docker run -it --rm --name python-denonavr -p 5567:5567 python-denonavr
# docker run --rm -p 5567:5567 toebsen/python-denonavr:latest