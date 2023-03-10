import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from accounts.models import User
from accounts.serializers import SignUpSerializer, LoginSerializer
from django.shortcuts import get_object_or_404


class SignUpAPIView(CreateAPIView):
    """
        회원가입 API View
        URL API : POST accounts/signup/
    """
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'data': serializer.data,
                "message": {
                    "msg": "You have successfully registered as a member!",
                    "status": "USER_CREATE_OK"
                }
            }, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'detail': '잘못된 형식 입니다.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
        로그인 API View
        URL API : POST accounts/login/
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    """
        API URL : GET accounts/login/
        access token을 decode 해서 유저 id 추출 => 유저 식별
        refresh 토큰 유효할시 access 토큰 다시 생성,
        아닐시 재로그인 유도 
    """

    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = LoginSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'detail':'토큰 유효기간이 끝났습니다. 로그인을 다시해주세요.'}, status=status.HTTP_403_FORBIDDEN)

        except jwt.exceptions.ExpiredSignatureError:
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = LoginSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res

        except jwt.exceptions.InvalidTokenError:
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """
        db 에 저장되어있는 유저가 확인되면
        refresh_token, access_token return,
        refresh_token, access_token 쿠키에 저장
    """

    def post(self, request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            serializer = LoginSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "data": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                    "message": {
                        "msg": "login success",
                        "status": "LOGIN_OK"
                    },
                },
                status=status.HTTP_200_OK,
            )
            response.set_cookie("access", access_token, httponly=True)
            response.set_cookie("refresh", refresh_token, httponly=True)
            return response
        return Response({'detail':'존재하지 않은 유저입니다.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
        로그아웃 API View
        URL API : POST accounts/logout/
    """
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    """
        JWT 인증이 된 유저가 요청을 보낼시
        쿠키에 저장된 토큰 삭제
    """

    def post(self, request):
        response = Response({
            "message": "Logout success"
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
