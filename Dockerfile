# Temporary solution to avoid docker hub pull limits
FROM quay.io/larsks/python:3.9

WORKDIR /app

ENV RUNNER_PLAYBOOK=create-projects.yaml
ENV PIPENV_VENV_IN_PROJECT=1

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
COPY requirements.yaml ./
RUN pipenv run ansible-galaxy collection install -r requirements.yaml -p collections

COPY . /app
CMD ["pipenv", "run", "python", "runner.py"]
