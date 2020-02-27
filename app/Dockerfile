FROM python:3.8

ENV PATH=$HOME/.local/bin:/usr/local/bin:/usr/src/app:$PATH

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# expose backend
EXPOSE 8080

CMD [ "python3.8", "./main.py" ]
