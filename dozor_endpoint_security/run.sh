virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
exit
sudo su
source venv/bin/activate
python3 flask-api/app/app.py &