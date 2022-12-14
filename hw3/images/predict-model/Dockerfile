FROM python:3.6

RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip install -r /build/requirements.txt

COPY predict_model.py /predict_model.py

ENTRYPOINT ["python", "predict_model.py"]
