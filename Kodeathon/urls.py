from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from portal import views


urlpatterns = [

    #IP:- 127.0.0.1:8000
    
    path('admin/', admin.site.urls),
    path('submitAndGetStatus', views.submit.as_view()),
    path('getSyntax', views.getSyntax, name="getSyntax"),
    path('editCode', views.editCode, name="editCode"),
    path('getResponse', views.getResponse, name="getResponse"),
    path('editNote', views.editNote, name="editNote"),
    path('saveDeleteCode', views.saveDeleteCode.as_view()),
    path('saveDeleteNote', views.saveDeleteNote.as_view())
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)