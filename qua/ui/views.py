import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User

from qua import utils


log = logging.getLogger('qua.' + __name__)


def index(request):

    return render(request, 'ui/index.html')


def password_reset(request, user_id):

    template = 'ui/reset_password.html'
    params = request.GET
    post = request.POST
    success = False

    if 'token' not in params:
        return redirect('/')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, template, {
            'error_message': 'Пользователь не существует'
        })

    if not utils.is_sign_ok(params['token'], '{0}-{1}'.format(user.id, user.password)):
        return render(request, template, {
            'error_message': 'Недействительный токен'
        })

    if 'password' in post:
        password = post.get('password', None)
        password_confirm = post.get('password_confirm', None)

        log.debug('Password: %s, password_confirm: %s', password, password_confirm)

        if password == '':
            return render(request, template, {
                'error_message': 'Пароль не может быть пустым'
            })

        if password and password != password_confirm:
            return render(request, template, {
                'error_message': 'Введенные пароли не совпадают'
            })

        user.set_password(password)
        user.save()

        success = True

    return render(request, template, {
        'user_id': user.id,
        'username': user.username,
        'error_message': None,
        'success': success
    })
