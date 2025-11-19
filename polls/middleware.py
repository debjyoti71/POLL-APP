from datetime import datetime
from .models import User

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_name = user.username
            except User.DoesNotExist:
                user_name = "Anonymous"
        else:
            user_name = "Anonymous"
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {request.method} {request.path} - User: {user_name}")
        
        response = self.get_response(request)
        return response