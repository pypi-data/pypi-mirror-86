# Django EVE Online Timerboard
A simple Django extension that offers timerboard functionality with EVE Online flavor.

# Installation
1. Add `django_eveonline_timerboard` to your INSTALLED_APPS
2. Include the `django_eveonline_timerboard` URLs in your urls.py
3. Run `python3 manage.py migrate` to create the django_eveonline_timerboard models

# Provided URLs
| URL Name | Description |
| ------------- | ------------- |
|  django-eveonline-timerboard-add-timer   | Add a timer |
|  django-eveonline-timerboard-remove-timer (int: timer_pk) | Remove a timer specified by timer_pk |
|  django-eveonline-timerboard-view  | View the timerboard |