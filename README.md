# VictorCarry
## Structure
```
├── README.md
├── db.sqlite3
├── elena
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── map_data.pkl (openstreetmap data for amherst)
├── route
│   ├── admin.py
│   ├── apps.py
│   ├── max_route.py (for max elevation)
│   ├── migrations
│   ├── min_route.py (for min elevation)
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py (handle user's request, call min/max elevation algo, return route)
├── static
│   └── assets
│       ├── css
│       ├── fonts
│       ├── img
│       └── js
└── templates
    └── hello_world.html (index html: user search UI, display route)

137 directories, 1836 files

```
## Requirements
Google API: Places API, Maps JavaScript API, Geocoding API, Maps Elevation API, Directions API <br>
Python Libraries: [googlemaps](https://github.com/googlemaps/google-maps-services-python), django
## Run
```
python manage.py runserver
```
