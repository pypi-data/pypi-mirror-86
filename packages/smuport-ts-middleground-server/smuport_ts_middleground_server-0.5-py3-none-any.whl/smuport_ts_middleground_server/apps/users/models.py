from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import django
# Create your models here.
from rest_framework.fields import JSONField

from data_apps.tlms_wms_public_table.models import ServiceProvider


class Menu(models.Model):
    """
    菜单表
    """
    GRADE = [
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级')
    ]
    title = models.CharField(max_length=50, unique=True, verbose_name="菜单")
    grade = models.IntegerField(choices=GRADE, default=1, verbose_name="菜单级别")
    parent = models.ForeignKey('self', null=True, blank=True, related_name="subClasses",
                               on_delete=models.CASCADE, verbose_name="父类目别")
    operate_user = models.CharField(default='admin', max_length=32, verbose_name="操作人")
    operate_date = models.DateTimeField(default=datetime.now, verbose_name="操作时间")

    class Meta:
        db_table = 'menu'
        verbose_name_plural = "菜单表"

    def __str__(self):
        # 显示层级菜单
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)


class Permission(models.Model):
    """
    权限
    """
    LEVEL = [
        (1, 'MODULE'),
        (2, 'SUBMODULE'),
        (3, 'PAGE'),
        (4, 'BUTTON')
    ]
    title = models.CharField(max_length=32, verbose_name="权限名称")
    url = models.CharField(max_length=128, unique=True, verbose_name="请求地址")
    codes = models.CharField(default='module', max_length=32, verbose_name="权限代码")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(choices=LEVEL, default=1, verbose_name="权限级别")
    operate_user = models.CharField(default='admin', max_length=32, verbose_name="操作人")
    operate_date = models.DateTimeField(default=datetime.now, verbose_name="操作时间")

    class Meta:
        db_table = 'permission'
        verbose_name_plural = '权限表'

    def __str__(self):
        # 显示带菜单前缀的权限
        return '{menu}---{permission}'.format(menu=self.menu, permission=self.title)


class Role(models.Model):
    """
    角色：绑定权限
    """
    title = models.CharField(max_length=32, unique=True)
    # 定义角色和权限的多对多关系
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name='角色的权限')
    operate_user = models.CharField(default='admin', max_length=32, verbose_name="操作人")
    operate_date = models.DateTimeField(default=datetime.now, verbose_name="操作时间")

    class Meta:
        db_table = 'role'
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, name=None, mobile=None, company=None, gender=None, apartment=None ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('请输入用户名！')
        user = self.model(username=username, name=name, mobile=mobile, gender=gender, apartment=apartment, company_id=company)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_user(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(default='admin', max_length=10, verbose_name="用户名")
    gender = models.CharField(choices=(('0', '男'), ('1', '女')), null=True, blank=True, max_length=1, verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    apartment = models.CharField(null=True, blank=True, max_length=20, verbose_name="部门")
    company = models.ForeignKey(ServiceProvider, verbose_name="公司", on_delete=models.CASCADE)
    # 定义用户和角色的多对多关系
    roles = models.ManyToManyField(Role)
    objects = UserManager()

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name
        db_table = "user"


class Auth(models.Model):
    Grade = (
        (0, '不可访问'),
        (1, '允许访问'),
        (2, '可修改'),
        (3, '高级修改')
    )
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    grade = models.IntegerField(choices=Grade, default=0, verbose_name="登记")

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = verbose_name
        db_table = "user_auth"

