from rest_framework.permissions import IsAuthenticated


class OrderPermission(IsAuthenticated):
    def has_permission(self, request, view):
        has_perm = super(OrderPermission, self).has_permission(request, view)
        if has_perm:
            has_perm = not request.user.is_superuser
        return has_perm

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user and obj.status == "WAITING"
