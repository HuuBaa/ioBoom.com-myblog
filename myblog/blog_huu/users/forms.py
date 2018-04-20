from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .fields import HoneyPotField, PasswordField, UsersEmailField
from django.contrib.auth.forms import PasswordChangeForm as pcf ,PasswordResetForm as prf,SetPasswordForm as spf
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

class SetPasswordForm(spf):
    error_messages = {
        'password_mismatch': _("两次密码不一致"),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )


class PasswordResetForm(prf):
    email = forms.EmailField(label=_("Email"), max_length=254,widget=forms.EmailInput(attrs={'class':'form-control'}))

class PasswordChangeForm(pcf):

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,'class':'form-control'}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )


class UserCreationForm(forms.ModelForm):

    error_messages = {
        'duplicate_email': _('邮箱已经被注册'),
        'password_mismatch': _('两次密码不一致'),
        'duplicate_username': _('用户名已经被使用'),
    }
    username=forms.CharField(label=_('用户名'),max_length=12,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = UsersEmailField(label=_('邮箱地址'), max_length=255,widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = PasswordField(label=_('密码'),widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = PasswordField(
        label=_('密码确认'),
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            get_user_model()._default_manager.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


    def clean_email(self):

        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username=self.cleaned_data['username']
        user.set_password(self.cleaned_data['password1'])
        user.is_active = not settings.USERS_VERIFY_EMAIL
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label=_('Password'), help_text=_(
        'Raw passwords are not stored, so there is no way to see '
        'this user\'s password, but you can change the password '
        'using <a href=\"password/\">this form</a>.'))

    class Meta:
        model = get_user_model()
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial['password']


class RegistrationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(
        label=_('I have read and agree to the Terms of Service'),
        widget=forms.CheckboxInput,
        error_messages={
            'required': _('You must agree to the terms to register')
        })


class RegistrationFormHoneypot(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a honeypot field
    for Spam Prevention

    """
    accept_terms = HoneyPotField()
