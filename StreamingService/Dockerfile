FROM python:3.7.0
COPY main.py ./
COPY stream_socket.py ./
COPY pipeline.py ./
COPY aircraft.avsc ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -la
CMD ["python", "./main.py"]
