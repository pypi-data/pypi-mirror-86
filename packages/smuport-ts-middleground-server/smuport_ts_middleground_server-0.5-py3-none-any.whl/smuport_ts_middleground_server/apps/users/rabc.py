from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.response import Response

from apps.users.models import Menu, Permission, Role
from apps.users.serializer import MenuSerializer, PermissionsSerializers, RoleSerializer
from utils.response import CommonResponseMixin, ReturnCode
from utils.yzModelViewSet import YzModelViewSet

User = get_user_model()


class MenuViewSet(YzModelViewSet, CommonResponseMixin):
    """
    菜单管理
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_menus_and_permissions(self, request):
        """
        创建菜单
        :param request: title，grade, parent, operate_user, url, per_code_title_list:list里面的元素是元祖
        :return: 创建成功
        """
        data = json.loads(request.body.decode())
        new_data = {}
        permission_level = 4

        """新增菜单"""
        # 菜单名唯一性验证
        new_data['title'] = data['title']
        if_redundant = Menu.objects.filter(title=data['title']).exists()
        if if_redundant:
            response = self.wrap_json_response(code=1002, message="'" + data['title'] + "' 已存在")
            return Response(response)
        new_data['grade'] = data['grade']
        if data['grade'] == '1':
            permission_level = 1
        if data['grade'] == '2':
            new_data['parent'] = Menu.objects.get(id=data['parent_id'])
            permission_level = 3
        new_data['operate_user'] = request.user.username
        menu = Menu.objects.create(**new_data)
        """新增权限"""
        per_obj = Permission()
        per_obj.title = menu.title
        per_obj.codes = data['code']
        per_obj.url = data.get('url', '')
        per_obj.level = permission_level
        per_obj.menu = menu
        per_obj.operate_user = request.user.name
        per_obj.save()

        # for per_code, per_title in per_code_title_list:
        #     temp_insert = Permission(
        #         title=per_title,
        #         codes=per_code,
        #         url=url + per_code + '/',
        #         menu=menu,
        #         operate_user=request.users.username
        #     )
        #     insert_per_list.append(temp_insert)
        # Permission.objects.bulk_create(insert_per_list)

        response = self.wrap_json_response()
        return Response(response)

    @action(methods=['put'], detail=False)
    def update_menus(self, request, *args, **kwargs):
        """
        更新菜单
        :param request: title，grade, parent, operate_user, url, per_code_title_list:list里面的元素是元祖
        :return: 创建成功
        """
        data = json.loads(request.body.decode())
        """更新菜单"""
        menu_obj = Menu.objects.get(id=kwargs.get('id'))
        menu_title = data['title']
        grade = data['grade']
        if grade == 2:
            parent = Menu.objects.get(id=data['parent_id'])
            menu_obj.parent = parent
        menu_obj.title = menu_title
        menu_obj.grade = grade
        menu_obj.operate_user = request.user.name
        menu = menu_obj.save()
        """更新权限"""
        per_obj = Permission.objects.get(id=data['permission_id'])
        per_obj.title = data['title']
        per_obj.codes = data['code']
        per_obj.url = data['url']
        per_obj.save()
        response = self.wrap_json_response()
        return Response(response)


class PermissionsViewSet(YzModelViewSet, CommonResponseMixin):
    """
    权限管理
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializers
    permission_classes = [IsAuthenticated]

    def query_permissions_tree(self, request):
        """
        查询权限树
        :param request: menu_id，codename, name
        :return: 创建成功
        """
        try:
            # 第一层：查询模块菜单资源
            menu = Menu.objects.filter(grade=1)
            nodes = []
            # 循环模块菜单资源找到对应权限
            for i in menu:
                ser = MenuSerializer(instance=i, many=False)
                node1 = {
                    'title': i.title,
                    'key': ser.data['permission_id'],
                    'menu_id': i.id,
                    'expanded': True,
                }
                node1_children = []
                # 第二层：根据模块菜单id查询对应页面菜单资源
                children_menu = Menu.objects.filter(parent=i, grade=2)
                if len(children_menu) > 0:
                    # 循环查找页面菜单资源对应的权限
                    for j in children_menu:
                        ser_j = MenuSerializer(instance=j, many=False)
                        node2 = {
                            'title': j.title,
                            'key': ser_j.data['permission_id'],
                            'menu_id': j.id,
                            'expanded': True,
                        }
                        node2_children = []
                        # 第三层：查找对应页面菜单资源的按钮权限
                        for leaf in ser_j.data['permissions']:
                            if leaf['level'] == 'BUTTON':
                                leaf_title = leaf['title']
                                node_leaf = {
                                    'title': leaf['title'],
                                    'key': leaf['id'],
                                    'isLeaf': True
                                }
                                node2_children.append(node_leaf)
                        node2['children'] = node2_children
                        node1_children.append(node2)
                    node1['children'] = node1_children
                else:
                    # 第二层：根据模块菜单id查询对应按钮菜单资源
                    ser_j = MenuSerializer(instance=i, many=False)
                    for leaf in ser_j.data['permissions']:
                        if leaf['level'] == 'BUTTON':
                            node_leaf = {
                                'title': leaf['title'],
                                'key': leaf['id'],
                                'isLeaf': True
                            }
                            node1_children.append(node_leaf)
                    node1['children'] = node1_children

                nodes.append(node1)

            response = self.wrap_json_response(data=nodes)
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="查询权限树失败！")
        return Response(response)

    def create_permissions(self, request):
        """
        创建权限
        :param request: menu_id，codename, name
        :return: 创建成功
        """
        try:
            data = json.loads(request.body.decode())
            print(data)
            menu = Menu.objects.get(id=data['menu_id'])
            insert_per_list = []
            code_arr = data['codes']
            title_arr = data['title']
            for i in range(len(code_arr)):
                url = data['url'] + code_arr[i] + '/'
                temp_insert = Permission(
                    title=title_arr[i],
                    codes=code_arr[i],
                    url=url,
                    menu=menu,
                    level=4,
                    operate_user=request.user.username
                )
                insert_per_list.append(temp_insert)
            Permission.objects.bulk_create(insert_per_list)
            # Permission.objects.create(**data)
            response = self.wrap_json_response()
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="创建权限失败！")
        return Response(response)

    def update_permissions(self, request, *args, **kwargs):
        """
        更新权限
        :param request: user_id：用户id，permission_list：权限列表
        :return: 保存结果
        """
        try:
            data = json.loads(request.body.decode())
            permission = Permission.objects.get(id=args)
            menu = Menu.objects.get(id=data['menu_id'])
            data['menu'] = menu
            permission.update(**data)
            response = self.wrap_json_response()
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="更新权限失败！")
        return Response(response)

    def user_remove_permissions(self, request):
        """
        用户删除权限
        :param request: user_id：用户id，permission_list：删除权限列表
        :return: 保存结果
        """
        try:
            data = json.loads(request.body.decode())
            user_id = data['user_id']
            permission_list = data['permission_list']
            user_obj = get_object_or_404(User, pk=user_id)
            print(user_obj.get_all_permissions())
            for per in permission_list:
                permission = Permission.objects.get(id=per)
                user_obj.user_permissions.remove(permission)
            print(user_obj.get_all_permissions())
            # 重新加载user 对象，获取最新权限
            user_obj_new = get_object_or_404(User, pk=user_id)
            print(user_obj_new.get_all_permissions())
            print(user_obj_new.get_group_permissions())
            response = self.wrap_json_response()
            pass
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="用户移除权限失败！")
        return Response(response)


class RoleViewSet(YzModelViewSet, CommonResponseMixin):
    """
    角色管理
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_role_and_permissions(self, request):
        """
        创建角色并绑定权限
        :param request: role:{}对象，permissions: [] 权限id列表
        :return: 创建成功
        """
        data = json.loads(request.body.decode())
        # 唯一性验证
        role_title = data['title']
        permissions = data['permissions']
        if_redundant = Role.objects.filter(title=role_title).exists()
        if if_redundant:
            response = self.wrap_json_response(code=1002, message="'" + role_title + "' 已存在")
            return Response(response)
        role_obj = Role.objects.create(
            title=role_title,
            operate_user=request.user.username
        )
        role_obj.permissions.add(*permissions)
        role_obj.save()
        response = self.wrap_json_response()
        return Response(response)

    @action(methods=['put'], detail=False)
    def update_role_and_permissions(self, request, *args, **kwargs):
        """
        更新角色权限
        :return: 更新成功
        """
        data = json.loads(request.body.decode())
        role_obj = Role.objects.get(id=kwargs.get('id'))
        role_title = data['title']
        role_obj.title = role_title
        # 更新权限
        permissions = data['permissions']
        role_obj.permissions.clear()
        role_obj.permissions.add(*permissions)
        role_obj.save()

        response = self.wrap_json_response()
        return Response(response)

    @action(methods=['put'], detail=False)
    def role_bind_users(self, request, *args, **kwargs):
        """
        角色配置用户
        :return: 更新成功
        """
        data = json.loads(request.body.decode())
        role_obj = Role.objects.get(id=kwargs.get('id'))
        users = data['users']
        role_obj.user_set.clear()
        role_obj.user_set.add(*users)
        role_obj.save()

        response = self.wrap_json_response()
        return Response(response)


# class GroupViewSet(viewsets.ModelViewSet, CommonResponseMixin):
#     """
#     权限组管理
#     """
#     queryset = Group.objects.all()
#     # serializer_class = GroupsSerializers
#
#     def create_group_and_permissions(self, request):
#         """
#         创建用户组并绑定权限
#         :param request: group_name: 用户组名称；permission_list[]: 权限列表
#         :return: 保存成功
#         """
#         try:
#             data = json.loads(request.body.decode())
#             group_name = data['group_name']
#             permission_list = data['permission_list']
#             group = Group.objects.create(
#                 name=group_name
#             )
#             for per in permission_list:
#                 permission = Permission.objects.get(id=per)
#                 group.permissions.add(permission)
#             response = self.wrap_json_response()
#         except Exception as e:
#             print(e)
#             response = self.wrap_json_response(code=1002, message="创建用户权限组失败！")
#         return Response(response)
#
#     def user_add_group(self, request):
#         """
#         用户绑定用户组
#         :param request: user_id: 用户ID，group_list[]: 权限组列表
#         :return: 绑定成功
#         """
#         try:
#             data = json.loads(request.body.decode())
#             user_id = data['user_id']
#             group_list = data['group_list']
#             user_obj = User.objects.get(id=user_id)
#             for g in group_list:
#                 group = Group.objects.get(id=g)
#                 user_obj.groups.add(group)
#             response = self.wrap_json_response()
#         except Exception as e:
#             print(e)
#             response = self.wrap_json_response(code=1002, message="用户组绑定失败！")
#         return Response(response)
