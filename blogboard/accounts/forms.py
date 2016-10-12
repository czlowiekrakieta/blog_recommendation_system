from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from blogs.models import UserFollowings

likes = [x for x in enumerate(['not at all', 'not so much', 'do not care', 'a bit', 'a lot'])]
User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
    path = forms.CharField(widget = forms.HiddenInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        path = self.cleaned_data.get('path')

        if username and password:
            user = User.objects.filter(username=username)

            if user.count() == 0:
                raise forms.ValidationError("no user like this")

            else:
                user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("incorrect password")

            if not user.is_active:
                raise forms.ValidationError("user not active")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def set_path(self, path):
        self.initial = {'path':path}

class UserLogoutForm(forms.Form):
    path = forms.CharField(widget = forms.HiddenInput)

    def clean(self, *args, **kwargs):
        path = self.cleaned_data.get('path')

        return super(UserLogoutForm, self).clean(*args, **kwargs)

    def set_path(self, path):
        self.initial = {'path':path}

class UserRegisterForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    email = forms.CharField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'email'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("password don't match")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("login taken")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email taken")

        return super(UserRegisterForm, self).clean(*args, **kwargs)

class UserLikesForm(forms.ModelForm):
    politics = forms.ChoiceField(choices=likes)
    sports = forms.ChoiceField(choices=likes)
    travel = forms.ChoiceField(choices=likes)
    fashion = forms.ChoiceField(choices=likes)
    culture = forms.ChoiceField(choices=likes)
    tech = forms.ChoiceField(choices=likes)
    soft_science = forms.ChoiceField(choices=likes)
    hard_science = forms.ChoiceField(choices=likes)

    class Meta:
        model = UserFollowings
        fields = [
            'politics',
            'sports',
            'fashion',
            'travel',
            'culture',
            'tech',
            'soft_science',
            'hard_science'
        ]

    def clean(self, *args, **kwargs):
        politics = self.cleaned_data.get("politics")
        travel = self.cleaned_data.get("travel")
        sports = self.cleaned_data.get("sports")
        culture = self.cleaned_data.get("culture")
        tech = self.cleaned_data.get("tech")
        soft_science = self.cleaned_data.get("soft_science")
        hard_science = self.cleaned_data.get("hard_science")
        fashion = self.cleaned_data.get("fashion")

        return super(UserLikesForm, self).clean(*args, **kwargs)
