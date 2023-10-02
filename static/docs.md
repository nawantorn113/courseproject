# Get start

- [Get start](#get-start)
  - [สร้างโปรเจค Django](#สร้างโปรเจค-django)
  - [สร้างแอพแรก](#สร้างแอพแรก)
  - [ตั้งค่าโปรเจค](#ตั้งค่าโปรเจค)
  - [เริ่มสร้างฐานข้อมูล](#เริ่มสร้างฐานข้อมูล)
  - [templates หน้าเว็บ](#templates-หน้าเว็บ)
  - [การใช้หน้าเว็บร่มกัน (extends)](#การใช้หน้าเว็บร่มกัน-extends)
  - [Views `views.py`](#views-viewspy)
  - [การสร้าง URL urls.py](#การสร้าง-url-urlspy)
  - [Deploy Vercel](#deploy-vercel)

## สร้างโปรเจค Django

- สร้างโปรเจค

```
django-admin startproject ชื่อโปรเจค
```

- เข้าไปยัง directory ของโปรเจค

```
cd ชื่อโปรเจค
```

- สร้างโฟลเดอร์สำหรับจัดเก็บ static file และ templates

```
mkdir static

mkdir templates
```

- สร้าง env

```
python -m venv env
```


- เปิด vscode ด้วย

```
code .
```
- เปิด terminal 
```
pip install django
pip install psycopg2
```
## สร้างแอพแรก

- เปิด terminal ใน vscode
- ใช้คำสั่งเพื่อสร้างแอพ

```
python manage.py startapp  ชื่อแอพ
```

## ตั้งค่าโปรเจค

- เขาไปที่ [settins.py](./resgis/settings.py)
- ตั้งค่า ALLOW_HOSTS

```python
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app']
```

- ตั้งค่า INSTALLED_APPS ให้เพิ่มชื่อแอพที่เราสร้างขึ้นใหม่

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
  
    'ชื่อแอพ',
]
```

- ตั้งค่า templates

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

- ตั้งค่าฐานข้อมูล

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ชื่อฐานข้อมูล",
        "USER": "ชื่อผู้ใช่",
        "PASSWORD": "รหัสผ่าน",
        "HOST": "ชื่อโฮสต์",
        "PORT": "5432",
    }
}
```

- ตั้งค่า static

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [Path.joinpath(BASE_DIR, 'static')]
STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles_build', 'static')
```

## เริ่มสร้างฐานข้อมูล

- เข้าไปยังแอพที่สร้างขึ้น [แอพ](./subject/)
- สร้าง ฐานข้อมูล ที่ไฟล์ [models.py](./subject/models.py)

```python
from django.db import models

# Create your models here.

# หมวดหมู่รายวิชา
class Category(models.Model):
    category = models.CharField(max_length=128) # ชื่อหมวดหมู่วิชาเรียน

    def __str__(self):
        return self.category


# รายวิชา
class Classes(models.Model):
    class_id = models.CharField(max_length=10) # รหัสรายวิชา
    class_name = models.CharField(max_length=128) # ชื่อรายวิชา
    class_credit = models.IntegerField() # หน่วยกิต
    class_year = models.IntegerField() # ปีการศึกษา
    semester = models.IntegerField() # ภาคเรียน  
    teacher = models.CharField(max_length=255) # คุณครูประจำวิชา
  
    class_category = models.ForeignKey(Category, on_delete=models.CASCADE) # หมวดหมู่รายวิชา

    on_register = models.BooleanField(default=False) # สถานะการเปิดการลงทะเบียน

    def __str__(self):
        return self.class_name
```

- register models ที่ [admin.py](./subject/admin.py)

```python
from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category'
    ]

@admin.register(models.Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = [
        'class_id',
        'class_name',
        'class_category',
        'on_register',
    ]

```

*การทำ admin register เพื่อที่เราจะสามารถเพิ่มข้อมูลเองได้*

หลังจากนั้นใช้คำสั่ง 
```
python manage.py makemigrations

python manage.py migrate
```


## templates หน้าเว็บ

- ให้หา Booststrap 5 template มาใช้
- เลือก `file.html` และย้ายไปที่ `templates/`
- เลือก `css/, js/ assets/` ย้ายไปยัง `static/`
- เข้าไปที่ `templates/` แล้วเลือกไฟล์ที่จะใช้เป็น `base.html`
- แล้วลบ tags ที่ไม่ใช้ออก
- เพิ่ม `{% load static %}` บนสุดของบรรทัด

```html
<!DOCTYPE html>
{% load static %}

<html>
    .
    .
    .

```

- เปลี่ยนการเชื่อมต่อ JavaScript และ CSS จากแบบเดิมเป็นแบบ Django Tempate

*จาก*

```html
 <link rel="stylesheet" href="assets/css/demo.css" />
 <script src="../assets/js/config.js"></script>
```

*เป็น*

```html
 <link rel="stylesheet" href="../{% static "assets/css/demo.css" %}" />
 <script src="../{% static "assets/js/config.js" %}"></script>
```

*ให้เปลี่ยนทุกตัว*

## การใช้หน้าเว็บร่มกัน (extends)

เป็การใช้องค์ประกอบหน้าเว็บจากหน้า `base.html` ร่วมกัน โดยจาเกปลี่ยนเพี่ยงแค่เนื้อหา
โดยใช้ Django Template Tags ที่ชื่อว่า

```html
{% block name %}{% endblock name %}
```

โดยหน้าที่ต้องการสืบทอดก็ใช้ Django Template Tags ที่ชื่อว่า

```html
{% extends 'base.html' %}

{% block name %}{% endblock name %}
```

แล้วก็ตามด้วยชื่อ block
ตัวอย่าง

`base.html`

```html
<html>
    <head>
        .
        .
        .
    </head>
    <body>
        <header>
        header
        </header>
            {% block name %}{% endblock name %}
        <footer>
        footer
        </footer>
</html>
```

`index.html`

```html
{% extends 'base.html' %}

{% block name %}
<h1>Hello</h1>
{% endblock name %}

```

ผลลัพ

```html
<html>
    <head>
        .
        .
        .
    </head>
    <body>
        <header>
        header
        </header>
            <h1>Hello</h1>
        <footer>
        footer
        </footer>
</html>
```

## Views [`views.py`](./subject/views.py)

[`views.py`](./subject/views.py) เป็นส่วนที่ควบคุมการทำงานของหน้าเว็บ การ render หน้าเว้บ

- สร้างฟังก์ชันสำหรับ render หน้า index

```python
def index(request):
    context = {}
    context['subjects'] = models.Classes.objects.all()
    return render(request, 'index.html', context)
```

`context` คือ ค่าที่จะส่งออกไปยังหน้าเว็บ มีรูปแบบเป็น dictionary

`context['subjects'] = models.Classes.objects.all()` คือ การดึงค่าทั้งหมดจากตาราง `Classes` ที่อยู่ใน ฐานข้อมูล

`return render(request, 'index.html', context)` คือ การรีเทิร์นค่าโดยสั่งให้ render หน้า `index.html` และยังส่ง `context` ออกไปยังหน้าเว็บ

- สร้างตารางใน [`index.html`](./templates/index.html)

```html
{% extends "base.html" %}

{% block content %}
<div class="card">
    <h5 class="card-header">Borderless Table</h5>
    <div class="table-responsive text-nowrap">
      <table class="table table-borderless">
        <thead>
          <tr>
            <th>รหัสวิชา</th>
            <th>รายวิชา</th>
            <th>หน่วยกิต</th>
            <th>หมวดหมู่</th>
            <th>ภาคเรียนที่</th>
            <th>ปีการศึกษา</th>
          </tr>
        </thead>
        <tbody>
        {% for item in subjects %}
          <tr>
            <td>{{item.class_id}}</td>
            <td>{{item.class_name}}</td>
            <td>{{item.class_credit}}</td>
            <td>{{item.class_category}}</td>
            <td>{{item.semester}}</td>
            <td>{{item.class_year}}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

{% endblock content %}
```

## การสร้าง URL [urls.py](./resgis/urls.py)

เป็นการสร้าง url เพื่อเรียกใช้ฟังกืชั่นใน views.py

- import แอพ เข้ามาทำงาน

```python
from django.contrib import admin
from django.urls import path
# แอพ
from subject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
]

```

- ใช้คำสั่ง runserver

```
python manage.py runserver
```

หากยังไม่มีข้อมูลก็จะไม่แสดงข้อมูล

## Deploy Vercel

- ตั้งค่า [wsgi.py](./resgis/wsgi.py)
```python
"""
WSGI config for resgis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resgis.settings')

application = get_wsgi_application()

app = get_wsgi_application()
```

เพิ่ม `app = get_wsgi_application()`

- สร้าง [vercel.json](vercel.json)

```json
{
    "version": 2,
    "builds": [
        {
            "src": "ชื่อโปรเจค/wsgi.py",
            "use": "@vercel/python"
        },
        {
            "src": "build_files.sh",
            "use": "@vercel/static-build",
            "config": {
                "distDir": "staticfiles_build"
            }
        }
    ],
    "routes": [
        {
            "src": "/static/(.*)",
            "dest": "/static/$1"
        },
        {
            "src": "/(.*)",
            "dest": "ชื่อโปรเจค/wsgi.py"
        }
    ]
  
}
```

- สร้าง [build_files.sh](build_files.sh)

```sh
python -m pip install --upgrade pip
pip install -r requirements.txt


python3.9 manage.py collectstatic --noinput --clear
```
- สร้าง `requirements.txt`
```
pip freeze > requirements.txt
```