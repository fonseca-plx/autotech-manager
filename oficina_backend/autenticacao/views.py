from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Usuario
from .serializers import UsuarioRegistroSerializer, UsuarioPerfilSerializer

class RegistroView(APIView):
    def post(self, request):
        serializer = UsuarioRegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"mensagem": "Usuário criado com sucesso!"}, status=201)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")
        usuario = authenticate(username=email, password=senha)

        if usuario is None:
            return Response({"erro": "Credenciais inválidas"}, status=400)

        refresh = RefreshToken.for_user(usuario)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "perfil": usuario.tipo_perfil
        })

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"mensagem": "Logout realizado com sucesso"})
        except Exception:
            return Response({"erro": "Token inválido"}, status=400)

class PerfilView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UsuarioPerfilSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UsuarioPerfilSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
