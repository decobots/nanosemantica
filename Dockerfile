FROM python:alpine
COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["waitress-serve", "--port", "8080", "src.falcon_app.app:app"]