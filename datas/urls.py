from django.urls import path

from datas import views

urlpatterns = [
    path('', view=views.card_view, name='card_view'),
    path('cate/', view=views.get_cate, name='get_cate'),
    path('link/', view=views.get_url, name='get_url'),
]