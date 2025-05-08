FROM public.ecr.aws/lambda/python:3.9

COPY ./api/image-upload/requirements.txt ./
RUN python3.9 -m pip install -r requirements.txt -t .

COPY ./api/image-upload/main.py ./
ADD ./rds ./rds

CMD ["main.lambda_handler"]
