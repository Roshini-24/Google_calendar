from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalendarInitView, name='init_view'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView, name='redirect_view'),
]
