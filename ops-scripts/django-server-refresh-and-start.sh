#/bin/bash
echo Refreshing code base and starting server...
git checkout -f fe-4 && git pull && python3 manage.py runserver 0.0.0.0:10000
echo Done!
