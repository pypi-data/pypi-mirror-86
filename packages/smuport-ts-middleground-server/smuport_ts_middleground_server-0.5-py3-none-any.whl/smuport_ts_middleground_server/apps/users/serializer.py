from apps.users.models import Permission
from . import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class PermissionsSerializers(serializers.ModelSerializer):
    """
    权限表序列化
    """
    menu_id = serializers.IntegerField(source="menu.id")
    menu_title = serializers.CharField(source="menu.title")
    level = serializers.CharField(source="get_level_display")

    class Meta:
        model = Permission
        fields = ('id', 'title', 'url', 'menu_id', 'menu_title', 'codes', 'level')


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单序列化类
    """
    grade_value = serializers.CharField(source="get_grade_display")
    permission_id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    codes = serializers.SerializerMethodField()
    parent_title = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    # 获取权限表对应URL
    def get_url(self, obj):
        if obj.grade == 1:
            per_obj = Permission.objects.filter(menu=obj)
        else:
            per_obj = Permission.objects.filter(menu=obj, level=3)
        ser = PermissionsSerializers(instance=per_obj, many=True)
        if len(ser.data) > 0:
            return ser.data[0]['url']
        else:
            return ''

    # 获取code
    def get_codes(self, obj):
        if obj.grade == 1:
            per_obj = Permission.objects.filter(menu=obj)
        else:
            per_obj = Permission.objects.filter(menu=obj, level=3)
        ser = PermissionsSerializers(instance=per_obj, many=True)
        if len(ser.data) > 0:
            return ser.data[0]['codes']
        else:
            return ''

    # 获取父级菜单id
    def get_parent_title(self, obj):
        if obj.parent is None:
            return ''
        else:
            return obj.parent.title

    # 获取权限id
    def get_permission_id(self, obj):
        if obj.grade == 1:
            per_obj = Permission.objects.filter(menu=obj)
        else:
            per_obj = Permission.objects.filter(menu=obj, level=3)
        ser = PermissionsSerializers(instance=per_obj, many=True)
        if len(ser.data) > 0:
            return ser.data[0]['id']
        else:
            return ''

    # 获取权限
    def get_permissions(self, obj):
        per_obj = Permission.objects.filter(menu=obj)
        ser = PermissionsSerializers(instance=per_obj, many=True)
        return ser.data

    class Meta:
        model = models.Menu
        fields = ('id', 'title', 'grade', 'grade_value', 'permission_id', 'url', 'codes', 'parent_id', 'parent_title',
                  'permissions')


class RoleSerializer(serializers.ModelSerializer):
    """
    角色序列化类
    """
    # 角色和权限多对多关系
    permissions = serializers.SerializerMethodField()
    permission_ids = serializers.SerializerMethodField()

    # 序列化用户组对应的权限
    # 钩子函数序列化必须以get_开头
    def get_permissions(self, obj):
        """
        :type obj: Role对象
        """
        if obj.permissions is not None:
            permission = obj.permissions.all()
            perm = PermissionsSerializers(permission, many=True)
            return perm.data
        else:
            return ''

    def get_permission_ids(self, obj):
        """
        :type obj: Role对象
        """
        if obj.permissions is not None:
            permission_ids = []
            permission = obj.permissions.all()
            for per in permission:
                if per.level == 3 or per.level == 4:
                    permission_ids.append(per.id)
            return permission_ids
        else:
            return []

    class Meta:
        model = models.Role
        fields = ('id', 'title', 'permissions', 'permission_ids')


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="工号", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=models.User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    class Meta:
        model = models.User
        fields = ("username", "name" "mobile", "password", "gender", "apartment")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    role_ids = serializers.SerializerMethodField()
    role_titles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    def get_role_ids(self, obj):
        """
        :type obj: users
        """
        if obj.roles is not None:
            role_ids = []
            role = obj.roles.all()
            for r in role:
                role_ids.append(r.id)
            return role_ids
        else:
            return []

    def get_role_titles(self, obj):
        """
        :type obj: users
        """
        if obj.roles is not None:
            role_titles = []
            role = obj.roles.all()
            for r in role:
                role_titles.append(r.title)
            return role_titles
        else:
            return []

    def get_permissions(self, obj):
        """
        :type obj: users
        """
        if obj.roles is not None:
            perms = {}
            module_perms = []
            page_perms = []
            page_button_perms = {}
            role = obj.roles.all()
            for r in role:
                permissions = r.permissions.all()
                for per in permissions:
                    if per.level == 1:
                        module_perms.append(per.codes)
                    elif per.level == 3:
                        page_perms.append(per.codes)
                        button_perms = []
                        perm_list = permissions.filter(menu_id=per.menu_id, level=4)
                        if len(perm_list) > 0:
                            for p in perm_list:
                                button_perms.append(p.codes)
                            page_button_perms[per.codes] = button_perms
            perms['module_perms'] = list(set(module_perms))
            perms['page_perms'] = list(set(page_perms))
            perms['page_button_perms'] = page_button_perms
            return perms
        else:
            return []

    class Meta:
        model = models.User
        fields = ("id", "username", "name", "gender", "apartment",  "mobile", "role_ids", "role_titles", "permissions", 'company')


class AuthSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    user = UserRegSerializer(read_only=True)

    class Meta:
        model = models.Auth
        fields = "__all__"

