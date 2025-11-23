from django.urls import path

from user.views.auth import UserRegister, UserLogin, UserLogout, Refresh
from user.views.user import UserOwnAccount, AdminUserManagement, AdminUserDetailManagement
from user.views.role import RoleView, RoleDetail
from user.views.permission import PermissionView, PermissionDetail

urlpatterns = [
    path('api/auth/register/', UserRegister.as_view(), name='register'),
    path('api/auth/login/', UserLogin.as_view(), name='login'),
    path('api/auth/logout/', UserLogout.as_view(), name='logout'),
    path('api/auth/refresh/', Refresh.as_view(), name="refresh-access-token"),
    
    path('api/users/me/', UserOwnAccount.as_view(), name="my-account"),

    path("api/admin/users/", AdminUserManagement.as_view(), name='admin-users-list'),
    path("api/admin/users/<int:user_id>/", AdminUserDetailManagement.as_view(), name='admin-update-user'),

    path("api/admin/roles/", RoleView.as_view(), name="roles"),
    path("api/admin/roles/<int:role_id>/", RoleDetail.as_view(), name="role-detail"),
    #УДАЛИТЬ ПЕРМИШН

    path("api/admin/permissions/", PermissionView.as_view(), name="permissions"),
    path("api/admin/permissions/<int:permission_id>/", PermissionDetail.as_view(), name="permission-detail"),

]
