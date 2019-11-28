# VictorCarry
## Structure
```
├── db.sqlite3
├── elena
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── route
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py (handle user's request, call min/max elevation algo, return route)
│   └── (Add a new .py file here, for min/max elevation algo)
└── templates
    └── hello_world.html (index html: user search UI, display route)
```
## Requirements
Google API: Places API, Maps JavaScript API, Geocoding API, Maps Elevation API, Directions API <br>
Python Libraries: [googlemaps](https://github.com/googlemaps/google-maps-services-python), django
## Run
```
python manage.py runserver
```
