FROM --platform=linux/amd64 python:3.7.15-slim

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY data_params data_params/
COPY utils utils/
COPY model model/
COPY main.py .

ENV PATH_TO_MODEL="model/csgo_model.cbm"
ENV NUM_FEATUERS=96

CMD ["python", "main.py"]