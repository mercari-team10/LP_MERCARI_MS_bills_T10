FROM python:3.7

WORKDIR /bills

COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . ./
ENTRYPOINT ["python", "bills.py"]

