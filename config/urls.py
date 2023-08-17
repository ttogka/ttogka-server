from django.contrib import admin
from django.urls import path, include

# from rest_framework import routers

from cards.views import SelectBrandView, CardListView, CardDetailView, CategoryRankView, AdvertiseView

# router = routers.DefaultRouter()
# router.register('posts', PostModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('datas.urls')),

    path('brand/', SelectBrandView.as_view(), name='brand-view'),
    path('brand/<int:pk>', CardListView.as_view(), name='card-list-view'),
    path('card/<int:pk>', CardDetailView.as_view(), name='card-detail-view'),
    path('rank/', CategoryRankView.as_view(), name='category-rank-view'),
    path('ad/', AdvertiseView.as_view(), name='advertise-view'),
]
