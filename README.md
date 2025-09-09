1. To add a new Django project, use terminal on the directory file and type "django-admin startproject nameoftheproject", and then type "python manage.py startapp main" to create main folder. Open settings.py inside project folder and add 'main' in INSTALLED_APPS. Add 6 subjects inside models.py based on what we told from the assignments, such as name, price, description, etc. Add some information code inside views.py so that it could be returned to main.html. Add index inside urls.py so that it could run the code inside views.py. Open PWS in browser and add new project, save the important information and then edit the environs, add DB_HOST, DB_NAME, etc which already have been shared via email, and PRODUCTION=True and SCHEMA=tugas_individu.

2. (Recommend to use "raw" button in github to see the diagram) 
HTTP Request      →       urls.py
                                ↓
models.py ← read/write data → views.py → HTTP Response (HTML)
                                ↑
                        Template (main.html)

3. settings.py is used so that we could connect our project and where we could see it (localhost and pws).

4. Database migration work if we want to add/change something inside models.py, so that the "change" will appear.

5. I think Django framework is the simplest and easiest than any other framework. And we use python so that our code is way more human readable and easy to handle.

6. So far i am satisfied with teaching assistant's work, because they always willing to help me if i have a problem or question about the tutorial.