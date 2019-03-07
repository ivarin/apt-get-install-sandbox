to run the tests in docker container:
```bash
mkdir apt-get-install-tests
cd apt-get-install-tests
git clone https://github.com/ivarin/apt-get-install-sandbox.git .
sudo docker build .
```

run it locally:
```bash
mkdir apt-get-install-tests
cd apt-get-install-tests
git clone https://github.com/ivarin/apt-get-install-sandbox.git .
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ --junitxml=./report.xml
```
hopefully, this will output [s]omething like this:
```
collected 11 items                                                                                                        

tests/test_apt_install.py ...........        
```
