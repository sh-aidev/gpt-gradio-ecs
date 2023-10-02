FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && rm -rf /root/.cache/pip

# ENV PATH="${PATH}:~/.local/bin"

COPY . /code/

EXPOSE 80

CMD ["python3", "demo.py"]