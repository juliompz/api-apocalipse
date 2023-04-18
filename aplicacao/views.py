from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from aplicacao.models import Sobrevivente, Inventario
from aplicacao.serializer import SobreviventeSerializer, InventarioSerializer


class SobreviventeViewSet(viewsets.ModelViewSet):
    """Exibindo todos sobreviventes"""

    queryset = Sobrevivente.objects.all()
    serializer_class = SobreviventeSerializer


class InventarioViewSet(viewsets.ModelViewSet):
    """Exibindo todos usuários"""

    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


class VotarInfectado(APIView):
    def put(self, request, id, format=None):
        sobrevivente = Sobrevivente.objects.get(pk=id)
        sobrevivente.votos_infectado+=1
        sobrevivente.save()
        if sobrevivente.votos_infectado >=3:
            sobrevivente.infectado = True
            sobrevivente.save()
            return Response({'mensagem': 'Sobrevivente sinalizado como infectado.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'mensagem': 'Voto registrado.'},
                            status=status.HTTP_200_OK)

class Comercio(APIView):

    ITENS_PONTOS = {
        'agua': 4,
        'alimento': 3,
        'medicacao': 2,
        'municao': 1,
    }

    def post(self, request, format=None):
        sobrevivente1_id = request.data.get('sobrevivente1_id')
        sobrevivente2_id = request.data.get('sobrevivente2_id')

        sobrevivente1 = Sobrevivente.objects.get(pk=sobrevivente1_id)
        sobrevivente2 = Sobrevivente.objects.get(pk=sobrevivente2_id)
    
        # Atualizar os itens dos sobreviventes envolvidos na troca
        sobrevivente1_itens = {
            'agua': sobrevivente1.inventario.agua,
            'alimento': sobrevivente1.inventario.alimento,
            'medicacao': sobrevivente1.inventario.medicacao,
            'municao': sobrevivente1.inventario.municao,
        }

        sobrevivente2_itens = {
            'agua': sobrevivente2.inventario.agua,
            'alimento': sobrevivente2.inventario.alimento,
            'medicacao': sobrevivente2.inventario.medicacao,
            'municao': sobrevivente2.inventario.municao,
        }

        sobrevivente1_itens_trocados = request.data.get('sobrevivente1_itens')
        sobrevivente2_itens_trocados = request.data.get('sobrevivente2_itens')

        pontos_sobrevivente1 = sum([self.ITENS_PONTOS[item] * quantidade for item, quantidade in sobrevivente1_itens_trocados.items()])
        pontos_sobrevivente2 = sum([self.ITENS_PONTOS[item] * quantidade for item, quantidade in sobrevivente2_itens_trocados.items()])

        if pontos_sobrevivente1 != pontos_sobrevivente2:
            return Response({'message': 'Os pontos dos itens ofertados pelos sobreviventes não são iguais.'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        for item, quantidade in sobrevivente1_itens_trocados.items():
            setattr(sobrevivente1.inventario, item, sobrevivente1.inventario.__dict__[item] - quantidade)
            setattr(sobrevivente2.inventario, item, sobrevivente2.inventario.__dict__[item] + quantidade)

        for item, quantidade in sobrevivente2_itens_trocados.items():
            setattr(sobrevivente2.inventario, item, sobrevivente2.inventario.__dict__[item] - quantidade)
            setattr(sobrevivente1.inventario, item, sobrevivente1.inventario.__dict__[item] + quantidade)
        
            
        sobrevivente1.inventario.save()
        sobrevivente2.inventario.save()

        sobrevivente1.inventario.refresh_from_db()
        sobrevivente2.inventario.refresh_from_db()
        
        return Response({'message': 'Troca realizada com sucesso.'})
