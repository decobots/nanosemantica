FROM python:alpine
COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt
RUN cd /opt/app
RUN python setup.py install
EXPOSE 8080
CMD ["waitress-serve", "--port", "8080", "nanosemantica_app.falcon_app.app:app"]