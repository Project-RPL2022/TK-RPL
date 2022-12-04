from accounts.models import HotelUser

def get_role(request):
    return HotelUser.objects.filter(user=request.user).values_list('role')[0][0]