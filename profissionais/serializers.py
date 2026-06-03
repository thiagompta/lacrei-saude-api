from rest_framework import serializers
from .models import Profissional


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

    def validate_contato(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Contato deve ter pelo menos 8 caracteres."
            )
        return value

    def validate_nome_social(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Nome social deve ter pelo menos 2 caracteres."
            )
        return value.strip()