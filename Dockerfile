FROM python:3.10-alpine

RUN pip install --upgrade pip

RUN adduser -D nonroot
RUN mkdir /app && chown -R nonroot:nonroot /app
WORKDIR /app

COPY --chown=nonroot:nonroot . .

RUN pip install virtualenv
RUN pip install telebot

USER nonroot

CMD virtualenv venv -p python
CMD ["source", "venv/bin/activate"]
CMD python neurobot.py
