from forms import LoginForm

def include_login_form(request):
    form = LoginForm()
    return {'login_form': form, 'login_form_layout': 'inline'}
