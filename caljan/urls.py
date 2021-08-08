from django.conf.urls import url
from caljan.views import *


urlpatterns = [
    url(r'api/add_feedback', add_feedback),
    url(r'api/get_menu', get_menu),
    url(r'api/', get_user_info),
    url(r'register', register_user),
    url(r'check_code', check_code),
    url(r'user_data', user_data),
    url(r'logout', logout),
    url(r'webhook_selector', webhook_selector),
    url(r'shedule_sign_up', shedule_sign_up),
    url(r'get_busy_shedule', get_busy_shedule)
]