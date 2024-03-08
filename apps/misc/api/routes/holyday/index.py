# views
from django.urls import path
from apps.misc.api.views.holyday.index  import HolydayAV

urlpatterns = [
    path('holyday', HolydayAV.as_view(), name='holyday'),
    path('holyday/<str:pk>', HolydayAV.as_view(), name='holyday'),
]