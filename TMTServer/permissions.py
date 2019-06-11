from rest_framework import permissions
import loginapp, tmtapp


class CustomerPermission(permissions.BasePermission):
    """
    自定义权限只允许对象的所有者编辑它。
    """

    def has_object_permission(self, request, view, obj):
        return True
        # 读取权限允许任何请求，
        # 所以我们总是允许GET，HEAD或OPTIONS请求。
        if request.method in permissions.SAFE_METHODS:
            return True

        # 只有该snippet的所有者才允许写权限。
        return False
        return obj.owner == request.user

    def has_permission(self, request, view):

        if request.method in ("HEAD", "OPTIONS"):
            return True

        if isinstance(view, loginapp.views.UserAuth):
            return True

        if isinstance(view, tmtapp.views_file.FileUploadObject):
            return True

        if isinstance(view, tmtapp.views_file.FileUploadBugObject):
            return True

        if isinstance(view, tmtapp.views_app_update.AppUploadObject):
            return True

        if request.session.get('user'):
            return True
        else:
            return False
