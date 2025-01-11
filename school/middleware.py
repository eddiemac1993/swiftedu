# middleware.py
from django.utils import timezone
from .models import UserActivityLog

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated before accessing request.user
        if hasattr(request, 'user') and request.user.is_authenticated:
            action = f"Accessed {request.path}"
            UserActivityLog.objects.create(
                user=request.user,
                action=action,
                details=f"Method: {request.method}, Path: {request.path}"
            )

        response = self.get_response(request)
        return response