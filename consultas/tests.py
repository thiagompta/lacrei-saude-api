from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from profissionais.models import Profissional
from .models import Consulta
from django.utils import timezone
from datetime import timedelta


class ConsultaTests(APITestCase):

    def setUp(self):
        # Cria usuário e autentica
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Cria profissional e consulta base
        self.profissional = Profissional.objects.create(
            nome_social='Dra. Base',
            profissao='Psicóloga',
            endereco='Rua Base, 1',
            contato='11999999999'
        )
        self.data_futura = timezone.now() + timedelta(days=7)
        self.consulta = Consulta.objects.create(
            data=self.data_futura,
            profissional=self.profissional
        )

    def test_criar_consulta(self):
        data = {
            'data': (timezone.now() + timedelta(days=10)).isoformat(),
            'profissional': self.profissional.id
        }
        response = self.client.post('/api/consultas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar_consultas(self):
        response = self.client.get('/api/consultas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_buscar_consulta_por_id(self):
        response = self.client.get(f'/api/consultas/{self.consulta.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_atualizar_consulta(self):
        data = {
            'data': (timezone.now() + timedelta(days=15)).isoformat(),
            'profissional': self.profissional.id
        }
        response = self.client.put(
            f'/api/consultas/{self.consulta.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deletar_consulta(self):
        response = self.client.delete(f'/api/consultas/{self.consulta.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_buscar_consultas_por_profissional(self):
        response = self.client.get(
            f'/api/consultas/por-profissional/{self.profissional.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_criar_consulta_data_passada(self):
        data = {
            'data': (timezone.now() - timedelta(days=1)).isoformat(),
            'profissional': self.profissional.id
        }
        response = self.client.post('/api/consultas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_consulta_sem_profissional(self):
        data = {
            'data': (timezone.now() + timedelta(days=5)).isoformat(),
        }
        response = self.client.post('/api/consultas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_acesso_sem_autenticacao(self):
        self.client.credentials()
        response = self.client.get('/api/consultas/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)