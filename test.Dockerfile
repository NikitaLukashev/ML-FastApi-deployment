FROM python:3.9

# Add python dependcies
COPY requirements.txt requirements.txt

# Create venv and install dependencies
RUN python3.9 -m venv allisone
RUN chmod u+x allisone/bin/activate
RUN ./allisone/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copy project
COPY alembic/ alembic/
COPY alembic.ini .
COPY data/ data/

ENV PYTHONPATH /src
COPY src src

# Run test
CMD alembic upgrade head \
    && pytest src/