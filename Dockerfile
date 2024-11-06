FROM python:3.12
ADD . /PIA-LENMOPRO
WORKDIR /PIA-LENMOPRO
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . 
EXPOSE 5000
CMD [ "python","main.py" ]