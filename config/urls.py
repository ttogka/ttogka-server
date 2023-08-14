from django.contrib import admin
from django.urls import path, include

from cards.views import SelectBrandView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('datas.urls')),
    path('brand/', SelectBrandView.as_view(), name='brand-view'),
]
