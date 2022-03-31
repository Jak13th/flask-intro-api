FROM python:3.9
WORKDIR /data
COPY . .
RUN pip install -r requirements.txt
EXPOSE 3300
CMD ["flask", "run", "--port=3300"]