
# Avoid shadowing the login() and logout() views below.

from django.utils.encoding import force_text

from django.utils.translation import ugettext_lazy as _


from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

from django.core.urlresolvers import reverse
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, QueryDict
from .compat import urlsafe_base64_decode
from .conf import settings
from .signals import user_activated, user_registered
from .utils import EmailActivationTokenGenerator, send_activation_email
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.tokens import default_token_generator
from django.utils.deprecation import (
    RemovedInDjango20Warning, RemovedInDjango21Warning,
)

import functools
import warnings

from .forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site


if settings.USERS_SPAM_PROTECTION:  # pragma: no cover
    from .forms import RegistrationFormHoneypot as RegistrationForm
else:
    from .forms import RegistrationForm

UserModel = get_user_model()


def deprecate_current_app(func):
    """
    Handle deprecation of the current_app parameter of the views.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if 'current_app' in kwargs:
            warnings.warn(
                "Passing `current_app` as a keyword argument is deprecated. "
                "Instead the caller of `{0}` should set "
                "`request.current_app`.".format(func.__name__),
                RemovedInDjango20Warning
            )
            current_app = kwargs.pop('current_app')
            request = kwargs.get('request', None)
            if request and current_app is not None:
                request.current_app = current_app
        return func(*args, **kwargs)
    return inner


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
@deprecate_current_app
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    warnings.warn("The password_reset_confirm() view is superseded by the "
                  "class-based PasswordResetConfirmView().",
                  RemovedInDjango21Warning, stacklevel=2)
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('输入新密码')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('密码重置失败')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@deprecate_current_app
@csrf_protect
def password_reset(request,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):
    warnings.warn("The password_reset() view is superseded by the "
                  "class-based PasswordResetView().",
                  RemovedInDjango21Warning, stacklevel=2)
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('密码重设'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@csrf_protect
@never_cache
def register(request,
             template_name='users/registration_form.html',
             activation_email_template_name='users/activation_email.html',
             activation_email_subject_template_name='users/activation_email_subject.html',
             activation_email_html_template_name=None,
             registration_form=RegistrationForm,
             registered_user_redirect_to=None,
             post_registration_redirect=None,
             activation_from_email=None,
             current_app=None,
             extra_context=None):

    if registered_user_redirect_to is None:
        registered_user_redirect_to = getattr(settings, 'LOGIN_REDIRECT_URL')

    # if request.user.is_authenticated():
    #         return redirect(registered_user_redirect_to)

    if not settings.USERS_REGISTRATION_OPEN:
        return redirect(reverse('users_registration_closed'))

    if post_registration_redirect is None:
        post_registration_redirect = reverse('users_registration_complete')

    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            if settings.USERS_AUTO_LOGIN_AFTER_REGISTRATION:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            elif not user.is_active and settings.USERS_VERIFY_EMAIL:
                opts = {
                    'user': user,
                    'request': request,
                    'from_email': activation_from_email,
                    'email_template': activation_email_template_name,
                    'subject_template': activation_email_subject_template_name,
                    'html_email_template': activation_email_html_template_name,
                }
                send_activation_email(**opts)
                user_registered.send(sender=user.__class__, request=request, user=user)
            return redirect(post_registration_redirect)
    else:
        form = registration_form()

    current_site = get_current_site(request)

    context = {
        'form': form,
        'site': current_site,
        'site_name': current_site.name,
        'title': _('注册'),
    }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


def registration_closed(request,
                        template_name='users/registration_closed.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('注册关闭'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


def registration_complete(request,
                          template_name='users/registration_complete.html',
                          current_app=None,
                          extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('注册完成'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


@never_cache
def activate(request,
             uidb64=None,
             token=None,
             template_name='users/activate.html',
             post_activation_redirect=None,
             current_app=None,
             extra_context=None):

    context = {
        'title': _('账户激活 '),
    }

    if post_activation_redirect is None:
        post_activation_redirect = reverse('users_activation_complete')

    UserModel = get_user_model()
    assert uidb64 is not None and token is not None

    token_generator = EmailActivationTokenGenerator()

    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.activate()
        user_activated.send(sender=user.__class__, request=request, user=user)
        if settings.USERS_AUTO_LOGIN_ON_ACTIVATION:
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # todo - remove this hack
            login(request, user)
            messages.info(request, '感谢注册，您现在已经成功登录！')
        return redirect(post_activation_redirect)
    else:
        title = _('邮件确认失败')
        context = {
            'title': title,
        }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


def activation_complete(request,
                        template_name='users/activation_complete.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('激活完成'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)



@sensitive_post_parameters()
@csrf_protect
@login_required
@deprecate_current_app
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    warnings.warn("The password_change() view is superseded by the "
                  "class-based PasswordChangeView().",
                  RemovedInDjango21Warning, stacklevel=2)
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, form.user)
            auth_logout(request)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('密码修改'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

@deprecate_current_app
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         extra_context=None):
    warnings.warn("The password_change_done() view is superseded by the "
                  "class-based PasswordChangeDoneView().",
                  RemovedInDjango21Warning, stacklevel=2)
    context = {
        'title': _('密码修改成功'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
