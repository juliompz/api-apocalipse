from django.db import models

    
class Inventario(models.Model):

    #Quantidade de agua
    agua = models.PositiveIntegerField(default=0)
    #Quantidade de alimentação
    alimento = models.PositiveIntegerField(default=0)
    #Quantidade de medicação
    medicacao = models.PositiveIntegerField(default=0)
    #Quantidade de munição
    municao = models.PositiveIntegerField(default=0)

    def calcular_pontos(self):
        return self.agua * 4 + self.alimento * 3 + self.medicacao * 2 + self.municao * 1

    

class Sobrevivente(models.Model):

    nome = models.CharField(max_length=255)
    idade = models.IntegerField()

    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino')
    )

    sexo = models.CharField(max_length=1, choices=SEXO, 
                            blank=False,null=False)

    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    infectado = models.BooleanField(default=False)
    votos_infectado = models.IntegerField(default=0)

    def __str__(self):
        return self.nome