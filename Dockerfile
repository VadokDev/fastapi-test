FROM public.ecr.aws/lambda/python:3.10
WORKDIR /var/task
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["app.main.handler"]