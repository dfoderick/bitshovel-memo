FROM python:2
ADD memo.py /
RUN pip install redis
CMD [ "python", "./memo.py" ]
