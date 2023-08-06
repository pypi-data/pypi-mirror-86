from django.contrib.auth.hashers import make_password
from django.db.models import F
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utils.response import CommonResponseMixin, ReturnCode
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from utils.yzModelViewSet import YzModelViewSet
from . import models
from .models import Role, Permission
from .serializer import UserDetailSerializer, AuthSerializer


# from django.contrib.auth import get_user_model
#
# User = get_user_model()

# Create your views here.


class AuthView(TokenObtainPairView, CommonResponseMixin):
    """
    登陆
    """
    def post(self, request, *args, **kwargs):
        # 获取serializer对象
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)  # 验证序列化的合法性，如果出错跑出异常
            response = self.wrap_json_response(data=serializer.validated_data)

        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED, message="用户名或密码错误，请重新登录")

        return Response(response)


class RefreshTokenView(TokenRefreshView, CommonResponseMixin):
    """
    更新token
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            response = self.wrap_json_response(data=serializer.validated_data)
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED, message="您提供的refresh-token已经失效")
        return Response(response)


class LogoutView(APIView, CommonResponseMixin):
    """
    退出登录
    """
    def post(self, request, *args, **kwargs):
        try:
            logout(request)
            response = self.wrap_json_response()
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED, message='请求异常，请检查错误。')
        return Response(response)


class RegisterView(APIView, CommonResponseMixin):
    """
    注册 使用自身的auth.User
    """
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser]

    #  前端输入用户名后，调取get接口验证username是否存在
    def get(self, request, *args, **kwargs):
        if_redundant = models.User.objects.filter(username=request.data['username']).exists()
        response = self.wrap_json_response(data=if_redundant)
        return Response(response)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            username = data.pop('username')
            name = data.pop('name')
            password = data.pop('password')
            models.User.objects.create_user(
                username, password, name
            )
            response = self.wrap_json_response()

        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=ReturnCode.SERVER_INTERNAL_ERROR, message='注册失败，请检查错误。')

        return Response(response)


class UserDetailView(YzModelViewSet, CommonResponseMixin):
    """
    用户详情
    """
    def get_queryset(self):
        return models.User.objects.filter(company=self.request.user.company.id)
    serializer_class = UserDetailSerializer

    @action(methods=['get'], detail=False)
    def query_user_by_id(self, request, *args, **kwargs):
        try:
            user_q_set = models.User.objects.filter(id=request.user.id)
            ser = UserDetailSerializer(instance=user_q_set, many=True)
            response = self.wrap_json_response(data=ser.data)
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=ReturnCode.SERVER_INTERNAL_ERROR, message='查询用户信息失败！')
        return Response(response)

    @action(methods=['post'], detail=False)
    def insert_user(self, request, *args, **kwargs):
        try:
            roles = request.data.pop('roles')
            username = request.data['username']
            password = request.data['password']
            name = request.data['name']
            mobile = request.data['mobile']
            company = request.user.company.id
            user = models.User.objects.create_user(
                username, password, name, mobile, company
            )
            user.roles.add(*roles)
            user.save()
            response = self.wrap_json_response()
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=ReturnCode.SERVER_INTERNAL_ERROR, message='新增用户失败，请检查错误。')
        return Response(response)

    @action(methods=['put'], detail=False)
    def update_users(self, request, *args, **kwargs):
        """
        更新用户
        :return: 更新成功
        """
        user = models.User.objects.filter(id=request.data['id'])
        user_obj = user.first()
        roles = request.data.pop('roles')
        user_obj.roles.clear()
        user_obj.roles.add(*roles)
        user.update(**request.data)
        response = self.wrap_json_response()
        return Response(response)


class AuthViewSet(YzModelViewSet):
    queryset = models.Auth.objects.all()  # 需要返回的结果集
    serializer_class = AuthSerializer  # 序列化



