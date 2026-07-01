from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Competicao, Calendario


@receiver(post_save, sender=Competicao)
def criar_ou_atualizar_calendario(sender, instance, created, **kwargs):
    """
    Sempre que uma Competicao for criada ou editada:
    - Cria o Calendario automaticamente (se não existir)
    - Atualiza a dataEvento se a data da competição mudar
    """
    calendario, foi_criado = Calendario.objects.get_or_create(
        competicao=instance,
        defaults={
            'dataEvento': instance.data,
            'horario': 'A definir',
        }
    )

    # Se já existia mas a data da competição mudou, sincroniza
    if not foi_criado and calendario.dataEvento != instance.data:
        calendario.dataEvento = instance.data
        calendario.save()