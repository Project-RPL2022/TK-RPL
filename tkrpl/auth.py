from accounts.models import HotelUser

def is_authenticated(request):
    '''Check if user in a session'''
    try:
        request.session["email"]
        return True
    except KeyError:
        return False

def get_role(request):
    return HotelUser.objects.filter(user=request.user).values_list('role')[0][0]