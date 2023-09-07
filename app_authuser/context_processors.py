from app_restapi.models import UserRegistration,User
from PostMan import common


# context processors for accessing course details for all templates

def user_data_links(request):
    context={}
    if common.is_authendicated(request):
        users = UserRegistration.objects.all()
        user = common.get_user(request.session['user_email'])
        print("user_id:", user.id)
        request.session['username'] = user.first_name
        try:
            user_data = UserRegistration.objects.get(user_id=user.id)

            context = {
                'user_data': user_data,
                'user': user,
                'users':users,
                'user_id': user.id,
            }
        except UserRegistration.DoesNotExist:
            return None
    return context
