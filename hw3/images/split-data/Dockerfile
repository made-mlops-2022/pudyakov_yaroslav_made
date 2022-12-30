FROM python:3.6

RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip install -r /build/requirements.txt

COPY split_data.py /split_data.py

ENTRYPOINT ["python", "split_data.py"]
