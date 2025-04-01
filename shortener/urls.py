from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'urls', views.URLViewSet, basename='url')

urlpatterns = [
    path('pstate',views.pstate,name="pstate"),
    path('', include(router.urls)),
    path('<str:short_code>', views.redirect_view, name='redirect'),
    
]