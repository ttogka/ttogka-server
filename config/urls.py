from django.contrib import admin
from django.urls import path, include

# from rest_framework import routers

from cards.views import SelectBrandView, CardListView, CardDetailView, CategoryRankView, AdvertiseView

# router = routers.DefaultRouter()
# router.register('posts', PostModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('datas.urls')),

    path('api/v1/brands/', SelectBrandView.as_view(), name='brand-view'),
    path('api/v1/brands/<int:pk>', CardListView.as_view(), name='card-list-view'),
    path('api/v1/cards/<int:pk>', CardDetailView.as_view(), name='card-detail-view'),
    path('api/v1/ranks/', CategoryRankView.as_view(), name='category-rank-view'),
    # path('ad/', AdvertiseView.as_view(), name='advertise-view'),
]
