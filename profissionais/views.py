import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Profissional
from .serializers import ProfissionalSerializer

logger = logging.getLogger(__name__)


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome_social', 'profissao']
    ordering_fields = ['nome_social', 'criado_em']

    def perform_create(self, serializer):
        logger.info(f"Criando profissional: {serializer.validated_data.get('nome_social')}")
        serializer.save()

    def perform_destroy(self, instance):
        logger.info(f"Removendo profissional: {instance.nome_social}")
        instance.delete()