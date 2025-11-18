from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {request.method} {request.path} - User: {user}")
        
        response = self.get_response(request)
        return response