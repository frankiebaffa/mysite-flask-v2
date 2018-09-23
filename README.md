# mysite-flask-v2  
These are the source files for the second iteration of my website hosted on
pythonanywhere.com. It is built to be a portfolio site for all of the projects
that I am currently working on: software, music, etc. The design of the website
is built for a single user or a pre-added set of users who would add content to
the page through the lite CMS.  
  
## Installation / Development Environment  
The following steps walk through cloning the repository, creating a python
virtual environment, installing the requirements, setting the environment
variable for the flask application, making the initial database migration,
and running the application.  
```
git clone https://github.com/frankiebaffa/mysite-flask-v2
cd mysite-flask-v2
```  
Create a virtual environment, I prefer using virtualenv:
```
virtualenv --python=/path/to/your/python3.6/interpreter virtualenvironmentname
source virtualenvironmentname/bin/activate
pip3.6 install -r requirements.txt
cd mysite
```
The following steps differ between Mac/Linux and Windows:  
  
Mac/Linux  
```
export FLASK_APP=frankiebaffa.py
```  

Windows  
```
set FLASK_APP=frankiebaffa.py
```  

Windows PowerShell  
```
$env:FLASK_APP = "frankiebaffa.py"
```  
  
```
flask db init
flask db migrate -m 'inital migration'
flask db upgrade
flask run
```

