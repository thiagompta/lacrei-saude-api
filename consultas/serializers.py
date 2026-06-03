from rest_framework import serializers
from .models import Consulta
from profissionais.serializers import ProfissionalSerializer


class ConsultaSerializer(serializers.ModelSerializer):
    profissional_detalhes = ProfissionalSerializer(
        source='profissional',
        read_only=True
    )

    class Meta:
        model = Consulta
        fields = ['id', 'data', 'profissional', 'profissional_detalhes',
                  'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']

    def validate_data(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError(
                "A data da consulta não pode ser no passado."
            )
        return value