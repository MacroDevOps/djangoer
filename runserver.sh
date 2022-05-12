rm -rf uwsgi.pid
uwsgi --ini uwsgi.ini
tail -f ./logs/uwsgi.log