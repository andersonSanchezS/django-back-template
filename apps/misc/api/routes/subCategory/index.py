# views
from django.urls import path
from apps.misc.api.views.subCategory.index  import SubCategoryAV

urlpatterns = [
    path('subCategory', SubCategoryAV.as_view(), name='subCategory'),
    path('subCategory/<str:pk>', SubCategoryAV.as_view(), name='subCategory_id'),
]