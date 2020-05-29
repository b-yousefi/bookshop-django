from rest_framework.permissions import BasePermission

from api.models import Order


class IsStaffOrTargetUser(BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action != 'list' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user


class IsStaffOrTargetUserObject(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            if int(request.data['user']) == request.user.id:
                return True
            else:
                return request.user.is_staff
        else:
            return view.action != 'list' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class IsStaffOrTargetOrderObject(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            order = Order.objects.get(id=request.data['order'])
            if request.user == order.user:
                return True
            else:
                return request.user.is_staff
        else:
            return view.action != 'list' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.order.user == request.user
