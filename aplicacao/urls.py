from django.urls import path, include
from rest_framework import routers

from aplicacao.views import SobreviventeViewSet, InventarioViewSet, VotarInfectado, Comercio

router = routers.DefaultRouter()

router.register('sobrevivente', 
                SobreviventeViewSet, 
                basename='Sobreviventes')




urlpatterns = [
    path('', include(router.urls)),
    path('sobrevivente/<int:id>/votar-infectado', VotarInfectado.as_view()),
    path('negociar/', Comercio.as_view())
]