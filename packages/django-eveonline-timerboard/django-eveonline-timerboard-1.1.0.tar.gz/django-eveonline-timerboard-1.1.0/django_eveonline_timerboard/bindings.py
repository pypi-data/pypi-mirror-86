from django.apps import apps 
from django.urls import reverse
from django.conf import settings
from packagebinder.bind import PackageBinding, SettingsBinding, TaskBinding, SidebarBinding
import logging 

logger = logging.getLogger(__name__)
app_config = apps.get_app_config('django_eveonline_timerboard')

def create_bindings():
    sidebar_bindings = apps.get_app_config('packagebinder').sidebar_bindings
    sidebar_bindings['django_eveonline_connector'].add_child_menu_item({
        "fa_icon": "fa-clock",
        "name": "Timerboard",
        "url": reverse("django-eveonline-timerboard-view"),
    })
