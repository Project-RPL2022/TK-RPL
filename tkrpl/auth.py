
def is_authenticated(request):
    '''Check if user in a session'''
    try:
        request.session["email"]
        return True
    except KeyError:
        return False