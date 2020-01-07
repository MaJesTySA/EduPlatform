from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequired():
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequired, self).dispatch(request, *args, **kwargs)