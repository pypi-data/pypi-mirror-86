from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.users import views
from apps.users.rabc import PermissionsViewSet, MenuViewSet, RoleViewSet
from apps.users.views import UserDetailView

app_name = 'apps.users'
urlpatterns = [
    url(r'^query-users/$', UserDetailView.as_view({"get": "query_user_by_id"})),
    # url(r'^get_button_perms/$', UserDetailView.as_view({"get": "get_button_perms_by_id"})),
    url(r'^insert-users/$', UserDetailView.as_view({"post": "insert_user"})),
    url(r'^update-users/(?P<id>\d+)?', UserDetailView.as_view({"put": "update_users"})),
    url(r'^create-menus/$', MenuViewSet.as_view({"post": "create_menus_and_permissions"})),
    url(r'^update-menus/(?P<id>\d+)?', MenuViewSet.as_view({"put": "update_menus"})),
    url(r'^query-perms-tree/$', PermissionsViewSet.as_view({"get": "query_permissions_tree"})),
    url(r'^create-perms/$', PermissionsViewSet.as_view({"post": "create_permissions"})),
    url(r'^create-roles/$', RoleViewSet.as_view({"post": "create_role_and_permissions"})),
    url(r'^update-roles/(?P<id>\d+)?', RoleViewSet.as_view({"put": "update_role_and_permissions"})),
    url(r'^users-add-perms/$', PermissionsViewSet.as_view({"post": "user_add_permissions"})),
    url(r'^users-remove-perms/$', PermissionsViewSet.as_view({"post": "user_remove_permissions"})),
    # url(r'^create-groups-perms/$', GroupViewSet.as_view({"post": "create_group_and_permissions"})),
    # url(r'^users-add-groups/$', GroupViewSet.as_view({"post": "user_add_group"}))
]


# 定义视图集的路由
router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionsViewSet, basename='permission')
# router.register(r'roles', GroupViewSet, basename='group')
urlpatterns += router.urls
