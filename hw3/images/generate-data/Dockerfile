FROM python:3.6

RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip install -r /build/requirements.txt

COPY generate_data.py /generate_data.py

ENTRYPOINT ["python", "generate_data.py"]
