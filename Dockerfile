FROM fnndsc/ubuntu-python3
COPY . /apt-get-install-tests
RUN pip install -r apt-get-install-tests/requirements.txt
RUN pytest apt-get-install-tests/tests/
