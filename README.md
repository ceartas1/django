# Django 
### Создайте виртуальную среду (venv) 
   
``` python -m venv venv ```
### активируйте venv
для windows
``` ./venv/Scripts/activate ```

для linux
``` sourse venv/bin/activate```

### установите зависимости 

``` pip install -r requirements/test.txt ``` для теста

``` pip install -r requirements/prod.txt ``` для запуска

``` pip install -r requirements/dev.txt ``` для разработки

### запустите проект 

``` cd lyceum```

``` python manage.py runserver```

