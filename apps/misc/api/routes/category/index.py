# views
from django.urls import path
from apps.misc.api.views.category.index  import CategoryAV

urlpatterns = [
    path('category', CategoryAV.as_view(), name='category'),
    path('category/<str:pk>', CategoryAV.as_view(), name='category'),
]