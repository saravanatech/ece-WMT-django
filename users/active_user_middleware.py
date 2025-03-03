from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now

from users.models import UserSession

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_paths = ['/user/login/', '/login/', '/user/fetch_user_data/']
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Token '):
            token = auth_header.split(' ')[1]
            try:
                if request.path not in login_paths: 
                    request.user = Token.objects.select_related('user').get(key=token).user
                    UserSession.objects.update_or_create(user=request.user, defaults={"last_activity": now()})
            except Token.DoesNotExist:
                request.user = AnonymousUser()
                print("❌ Token Authentication Failed: Invalid token")
        return self.get_response(request)