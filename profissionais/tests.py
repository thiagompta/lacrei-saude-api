from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profissional


class ProfissionalTests(APITestCase):

    def setUp(self):
        # Cria usuário e autentica antes de cada teste
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

        # Cria um profissional base para os testes
        self.profissional = Profissional.objects.create(
            nome_social='Dr. Teste',
            profissao='Médico',
            endereco='Rua Teste, 1',
            contato='11999999999'
        )

    def test_criar_profissional(self):
        data = {
            'nome_social': 'Dra. Maria',
            'profissao': 'Psicóloga',
            'endereco': 'Av. Brasil, 100',
            'contato': '11988888888'
        }
        response = self.client.post('/api/profissionais/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome_social'], 'Dra. Maria')

    def test_listar_profissionais(self):
        response = self.client.get('/api/profissionais/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_buscar_profissional_por_id(self):
        response = self.client.get(f'/api/profissionais/{self.profissional.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome_social'], 'Dr. Teste')

    def test_atualizar_profissional(self):
        data = {
            'nome_social': 'Dr. Teste Atualizado',
            'profissao': 'Especialista',
            'endereco': 'Rua Nova, 2',
            'contato': '11977777777'
        }
        response = self.client.put(
            f'/api/profissionais/{self.profissional.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profissao'], 'Especialista')

    def test_deletar_profissional(self):
        response = self.client.delete(f'/api/profissionais/{self.profissional.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_criar_profissional_sem_nome(self):
        data = {
            'profissao': 'Médico',
            'endereco': 'Rua X',
            'contato': '11999999999'
        }
        response = self.client.post('/api/profissionais/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_profissional_contato_curto(self):
        data = {
            'nome_social': 'Dr. X',
            'profissao': 'Médico',
            'endereco': 'Rua X',
            'contato': '123'
        }
        response = self.client.post('/api/profissionais/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_acesso_sem_autenticacao(self):
        self.client.credentials()  # Remove o token
        response = self.client.get('/api/profissionais/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)