FROM python:3.6

RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip install -r /build/requirements.txt

COPY train_model.py /train_model.py

ENTRYPOINT ["python", "train_model.py"]
