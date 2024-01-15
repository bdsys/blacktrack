* Blacktrack:
    - Launch:
        - python3 /home/ssm-user/blacktrack/blacktrack/manage.py runserver 0.0.0.0:10000

    - https://blacktrack-dev.django-dev.bdsys.net/
        -  ALB

    - http://ec2-3-133-119-202.us-east-2.compute.amazonaws.com:10000/
        - fleet member server
        
        https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
        https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m
        https://docs.djangoproject.com/en/3.2/topics/auth/passwords/
        
        
* PGadmin4
   - Launch:
       - sudo service apache2 start
           - status for troubleshooting
       - https://django-dev.bdsys.net:8443/pgadmin4/
#

* SSH IAM User key
    - https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html

* Try this out when setting up CI/CD
    - https://aws.amazon.com/blogs/devops/complete-ci-cd-with-aws-codecommit-aws-codebuild-aws-codedeploy-and-aws-codepipeline/

* List of PostgreSQL web administration clients:
    - https://wiki.postgresql.org/wiki/PostgreSQL_Clients#Open_Source_2
        - PGadmin web - https://www.pgadmin.org/download/pgadmin-4-apt/
        - OmniDB (runs on Django) - https://omnidb.readthedocs.io/en/latest/en/02_installation.html

* Setting up PostgreSQL in Django
    - Enter into your project's venv
        - workon < venv name here >

    - Download PostgreSQL Python library
        - pip install psycopg2-binary

#

* Setting up environment
(https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment)

    - Initialize apt
        - sudo apt update

    - Install pip3
        - sudo apt install python3-pip
        
    - Install virtualwrapper
        - sudo pip3 install virtualenvwrapper
    
    - vim ~/.bashrc
    --  export WORKON_HOME=$HOME/.virtualenvs
        export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
        export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
        export PROJECT_HOME=$HOME/Devel
        source /usr/local/bin/virtualenvwrapper.sh
    
    - Compile bashrc
        - source ~/.bashrc
        
    - Create virtualenv
        - cd ~
        - mkvirtualenv my_django_environment
        
    (Assuming to be inside of venv...)
    
    - Install Django (with fuzzy pin)
        - pip3 install django~=3.1
        - python3 -m django --version
            - This tests the install and prints version

#

* Updating remote server fleet member
    - If on non-master branch
        - git checkout -f master
        - git pull origin master
        - git fetch
        - git pull < new branch name >
        - git checkout < new branch name >

    - If on master
        - git reset --hard HEAD
        - git pul origin master
        
        
#

* Data model maintenance
    - You'll need to run these commands every time your models change in a way that will affect the structure of the data that needs to be stored (including both addition and removal of whole models and individual fields).
        - Relative to the directory that contains manage.py 
            - python3 manage.py makemigrations
            - python3 manage.py migrate

