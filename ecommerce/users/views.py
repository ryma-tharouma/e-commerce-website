from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes

from .serializers import RegisterSerializer, UserProfileSerializer

# Register View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

# Login View
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=400)

# Profile View
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access profile
def profile_view(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


# from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from rest_framework.decorators import api_view, permission_classes
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# from .serializers import RegisterSerializer, UserProfileSerializer

# # Register View (CSRF exempt since used from frontend)
# @method_decorator(csrf_exempt, name='dispatch')
# class RegisterView(generics.CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = RegisterSerializer

# # Login View (CSRF exempt since used from frontend)
# @method_decorator(csrf_exempt, name='dispatch')
# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)

#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response({'error': 'Invalid credentials'}, status=400)

# # Profile View (requires JWT in Authorization header)
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def profile_view(request):
#     serializer = UserProfileSerializer(request.user)
#     return Response(serializer.data)
