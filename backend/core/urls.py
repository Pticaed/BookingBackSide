"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from booking import views_property, views_review, views_price, views_booking

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users
    path('api/users/', user_views.user_list, name='user_list'),
    path('api/users/create/', user_views.user_create, name='user_create'),
    path('api/users/<str:wallet_address>/', user_views.user_detail, name='user_detail'),
    path('api/users/<str:wallet_address>/update/', user_views.user_update, name='user_update'),
    path('api/users/<str:wallet_address>/delete/', user_views.user_delete, name='user_delete'),

    # Properties
    path('api/properties/', views_property.property_list, name='property_list'),
    path('api/properties/create/', views_property.property_create, name='property_create'),
    path('api/properties/<uuid:pk>/', views_property.property_detail, name='property_detail'),
    path('api/properties/<uuid:pk>/update/', views_property.property_update, name='property_update'),
    path('api/properties/<uuid:pk>/delete/', views_property.property_delete, name='property_delete'),
    path('api/properties/<uuid:pk>/availability/', views_property.property_availability, name='property_availability'),

    # Price History
    path('api/properties/<uuid:pk>/price-history/', views_price.property_price_history, name='property_price_history'),
    path('api/price-history/create/', views_price.price_history_create, name='price_history_create'),

    # Reviews
    path('api/bookings/<uuid:booking_id>/reviews/', views_review.booking_reviews, name='booking_reviews'),
    path('api/reviews/create/', views_review.review_create, name='review_create'),
    path('api/reviews/<uuid:pk>/update/', views_review.review_update, name='review_update'),
    path('api/reviews/<uuid:pk>/delete/', views_review.review_delete, name='review_delete'),
    
    # Bookings
    path('api/bookings/', views_booking.booking_list, name='booking_list'),
    path('api/bookings/create/', views_booking.booking_create, name='booking_create'),
    path('api/bookings/<uuid:pk>/update/', views_booking.booking_update, name='booking_update'),
    path('api/bookings/<uuid:pk>/delete/', views_booking.booking_delete, name='booking_delete'),
]