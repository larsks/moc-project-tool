FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY requirements.yaml /app/requirements.yaml
RUN ansible-galaxy collection install -r requirements.yaml -p collections

COPY . /app
ENTRYPOINT ["ansible-playbook", "create-projects.yaml"]
