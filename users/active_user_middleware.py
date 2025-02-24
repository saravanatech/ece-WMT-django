from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from datetime import datetime

from users.models import UserActivity

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Token '):
            token = auth_header.split(' ')[1]
            try:
                request.user = Token.objects.get(key=token).user.id
                UserActivity.objects.filter(id=request.user).update(last_activity=datetime.now())
            except Token.DoesNotExist:
                request.user = AnonymousUser()
                print("❌ Token Authentication Failed: Invalid token")
        return self.get_response(request)