from .models import User

def current_user(request):
    user_id = request.session.get('user_id')
    print(f"DEBUG: context_processor - session user_id: {user_id}")
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            print(f"DEBUG: context_processor - found user: {user.username}")
            return {'current_user': user}
        except User.DoesNotExist:
            print("DEBUG: context_processor - user not found in database")
            pass
    return {'current_user': None}