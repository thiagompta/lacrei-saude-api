import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Consulta
from .serializers import ConsultaSerializer

logger = logging.getLogger(__name__)


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['data', 'criado_em']

    def perform_create(self, serializer):
        logger.info(f"Criando consulta para profissional ID: {serializer.validated_data.get('profissional').id}")
        serializer.save()

    @action(detail=False, methods=['get'], url_path='por-profissional/(?P<profissional_id>[^/.]+)')
    def por_profissional(self, request, profissional_id=None):
        consultas = Consulta.objects.filter(profissional_id=profissional_id)
        serializer = self.get_serializer(consultas, many=True)
        logger.info(f"Buscando consultas do profissional ID: {profissional_id}")
        return Response(serializer.data)