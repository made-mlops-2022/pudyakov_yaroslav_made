FROM python:3.6

RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip install -r /build/requirements.txt

COPY process_data.py /process_data.py

ENTRYPOINT ["python", "process_data.py"]
