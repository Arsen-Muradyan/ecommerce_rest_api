from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v3/', include('products.urls')),
    path('api/v3/', include('marketing.urls')),
    path('api/v3/', include('accounts.urls')),
    path('api/v3/', include('cart.urls')),

]
