from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from aplicacao.models import Sobrevivente, Inventario

class InventarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Inventario
        fields = ('agua', 'alimento', 'medicacao', 'municao')


class SobreviventeSerializer(serializers.ModelSerializer):
    
    inventario = InventarioSerializer(many=False)

    class Meta:
        model = Sobrevivente
        fields = ('id','nome', 'idade', 'sexo', 'infectado', 'votos_infectado','latitude', 'longitude', 'inventario')


    def create(self, validated_data):
        inventario_data = validated_data.pop('inventario')
        inventario = Inventario.objects.create(**inventario_data)
        sobrevivente = Sobrevivente.objects.create(inventario=inventario, **validated_data)
        return sobrevivente

    def update(self, instance, validated_data):
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()

        return instance
