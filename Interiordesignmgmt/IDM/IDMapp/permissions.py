from rest_framework.permissions import IsAuthenticated,BasePermission

# models.py
from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)

class AgentPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            logger.info(f"Authenticated user: {request.user.username}, user_type: {request.user.user_type}")
            return request.user.user_type == 'agent'
        return False

# class CustomerPermissions(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             logger.info(f"Authenticated user: {request.user.username}, user_type: {request.user.user_type}")
#             return request.user.user_type == 'customer'
#         return False