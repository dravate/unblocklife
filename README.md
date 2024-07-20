# unblocklife - CMS System Name 

This is based on Wagtail CMS.  The Wagtail comes with several built-in features to support users with accessibility needs and an accessibility checker to encourage accessible content creation. We are also proud Wagtail CMS is a trusted tool used by the Royal National Institute of Blind People.

## Installing this instance

```
git clone git@github.com:dravate/unblocklife.git
cd unblocklife
pipenv --python /usr/bin/python3
pipenv shell
pip install -r requirements.txt 
python manage.py makemigrations home courses 
python manage.py migrate
python manage.py runsever

```

You can access the site at ```http://localhost:8000``` 



