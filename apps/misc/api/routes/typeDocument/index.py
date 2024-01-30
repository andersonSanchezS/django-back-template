# views
from django.urls import path
from apps.misc.api.views.typeDocument.index  import TypeDocumentAV

urlpatterns = [
    path('typeDocument', TypeDocumentAV.as_view(), name='typeDocument'),
]