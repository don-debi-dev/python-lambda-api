FROM public.ecr.aws/lambda/python:3.9

COPY ./api/test-ep/requirements.txt ./
RUN python3.9 -m pip install -r requirements.txt -t .

COPY ./api/test-ep/main.py ./
ADD ./rds ./rds

CMD ["main.lambda_handler"]
