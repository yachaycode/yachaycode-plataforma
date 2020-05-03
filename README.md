### YachayCode
![Arquitectura](arquitectura-yachaycode.png)

YachaCode es una plataforma de gestión de contenido(CMS) minimal. Construido utilizando el marco Django, YachaCode proporciona una arquitectura potente para generar contenido de blog totalmente administrable y escalable.

### Requisitos:
- git
- pip3 
- virtualenv 
- python3 
- postgresql-9.5

### Ejecución en modo desarrollo:

```
git clone git@gitlab.com:iisotec/yachaycode.git
```
```
cp yachaycode/yachaycode/settings/config_example.json yachaycode/yachaycode/settings/config.json && cd yachaycode
```
```
pip install -r install requeriments.txt
```
Confgurar su DB, antes de ejecutar las migraciones.. 

```
./manage.py makemigrations users && ./manage.py makemigrations blog  && ./manage.py makemigrations seo && ./manage.py migrate
```
```
./manage.py createsuperuser
```
```
 ./manage.py runserver
```
