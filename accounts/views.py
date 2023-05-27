from random import randint
from rest_framework import generics, status, permissions, response, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .utils import verify
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, ResetPasswordSerializer, \
    UserSerializer, VerifyPhoneSerializer
from .models import User, VerifyPhone


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        phone = self.request.data['phone']
        if User.objects.filter(phone=phone, is_active=True).first():
            return response.Response({'message': "This number already exist"}, status=status.HTTP_302_FOUND)
        code = str(randint(1000, 10000))
        if not VerifyPhone.objects.filter(phone=phone):
            verify(phone, code)
        VerifyPhone.objects.create(phone=phone, code=code)
        return response.Response({"success": True, 'message': "A confirmation code was sent to the phone number!!!"},
                                 status=status.HTTP_200_OK)


class RegisterConfirmAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = VerifyPhoneSerializer

    def post(self, request, *args, **kwargs):
        phone = self.request.data['phone']
        password = self.request.data['password']
        code = self.request.data['code']
        name = self.request.data['name']
        last_name = self.request.data['last_name']
        v = VerifyPhone.objects.filter(phone=phone, code=code).first()
        if v:
            v.delete()
        else:
            return response.Response({'message': "Confirmation code incorrect!"}, status=status.HTTP_400_BAD_REQUEST)
        user_n = User.objects.filter(phone=phone).first()
        if user_n:
            user_n.is_active = True
            user_n.save()
            token = Token.objects.create(user=user_n)
            data = {
                'message': 'User verified',
                'token': str(token.key),
                'role': user_n.role
            }
        else:
            user = User.objects.create_user(
                phone=phone,
                password=password,
                last_name=last_name,
                name=name
            )
            user.is_active = True
            user.save()
            token = Token.objects.create(user=user)
            data = {
                'message': 'User verified',
                'token': str(token.key),
                'role': user.role
            }
        return response.Response(data, status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = self.request.data['phone']
            password = self.request.data['password']
            user = User.objects.filter(phone=phone).first()
            if not user:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(phone=phone, password=password)
            if not user:
                return Response({"message": 'Password is incorrect'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {'Phone': phone, 'token': token.key, 'role': user.role})
        return Response({'success': False, 'message': 'Phone or password is invalid'},
                        status=status.HTTP_404_NOT_FOUND)


class ChangePasswordAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        user = request.user
        pas1 = self.request.data['password']
        user.set_password(pas1)
        user.save()
        return response.Response({'success': True, 'message': 'Successfully changed password'})


class UserAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=self.request.user, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = str(randint(1000, 10000))
        verify(phone, code)
        VerifyPhone.objects.create(phone=phone, code=code)
        return response.Response({"success": True, 'message': "A confirmation code was sent to the phone number!!!"})


class VerifyPhoneResetPasswordAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        phone = self.request.data['phone']
        code = self.request.data['code']
        v = VerifyPhone.objects.filter(phone=phone, code=code).first()
        if v:
            v.delete()
        else:
            return response.Response({'message': "Confirmation code incorrect!"}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({'message': "Successfully verified!"})


class ResetPasswordConfirmAPI(views.APIView):

    def post(self, request, *args, **kwargs):
        phone = self.request.data['phone']
        password = self.request.data['password']
        user = User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
        return response.Response({'success': True, 'message': "Password restored"})
