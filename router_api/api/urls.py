from django.urls import path, include
from .views import RouterDetail, RouterData, AddData, login

urlpatterns = [
    path('login', login),
    path('fetch_router/', RouterDetail.as_view()),
    path('get_router/<int:router_id>/', RouterData.as_view()),
    path('add/', AddData.as_view()),
    path('update/<int:router_id>', RouterData.as_view()),
    path('delete/<int:router_id>/', RouterDetail.as_view()),
    
]