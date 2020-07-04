from .import views
from django.urls import path

urlpatterns = [
    path('', views.index,name="shophome"),
    path('about/', views.about,name="aboutus"),
    path('contact/', views.contact,name="contactus"),
    path('tracker/', views.tracker,name="trackingstatus"),
    path('search/', views.search,name="search"),
    path('products/<int:myid>', views.productview,name="product"),
    path('products/<int:myid>', views.productview,name="product"),
    path('checkout/', views.checkout,name="checkout"),
    path('handlerequest/', views.handlerequest,name="handlerequest")
]
