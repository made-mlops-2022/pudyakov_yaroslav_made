В рамках данного домашнего задания я использовал независимую от первого дз задачу и модель (на консультации сказали, что такое вполне можно делать).
Я обучил [catboost.CatBoostClassifier](https://catboost.ai/en/docs/concepts/python-reference_catboostclassifier) модель для классификация стороны-победителя в игре csgo.
[Датасет](https://www.kaggle.com/datasets/christianlillelund/csgo-round-winner-classification) взят с сайта kaggle.

#### Сборка образа и запуск контейнера

Docker container building:

```bash
docker build -f Dockerfile -t csgo_fastapi . 
docker run -p 8000:8000 -d csgo_fastapi
```

Но я написал специальный скрипт, `scripts/build_and_run.sh` который подтягивает образ из [docker hub](https://hub.docker.com/r/boomland/csgo_fastapi) и запускает контейнер с необходимыми параметрами (можно изменять)
Запустить скрипт можно следующим образом:
```bash
chmod +x scripts/*
scripts/build_and_run.sh
```

Для запуска запросов `predict` необходимо запустить скрипт `scripts/send_requests.py` (убедитесь, что была воспроизведена команда `chmod +xscripts/*` ранее).
Для построяния предсказания в качестве пререквизитов необходимы две библиотеки `requests==2.28.1` и `pandas==1.4.3`


#### Самопроверка:

1) done (3)
2) done (1)
3) \- (3)
4) done (2)
5) done (4)
6) done (2)
7) done (1)
8) done (1)

Бонусные задания: \-

**Total**: 14 \
**Total** (hard deadline submission): 8.4
