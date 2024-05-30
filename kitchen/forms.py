from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    PasswordResetForm,
    UserCreationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError
from django.forms import SelectMultiple
from django.utils.translation import gettext_lazy as _

from kitchen.models import Cook, Dish, DishType, Ingredient


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Password"}
        ),
    )


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Old Password",
            }
        ),
        label="Old Password",
    )
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "New Password",
            }
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Confirm New Password",
            }
        ),
        label="Confirm New Password",
    )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "New Password",
            }
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Confirm New Password",
            }
        ),
        label="Confirm New Password",
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Email"}
        )
    )


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password Confirmation",
            }
        ),
    )

    class Meta:
        model = Cook
        fields = (
            "username",
            "email",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Username",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control form-control-lg", "placeholder": "Email"}
            ),
        }


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "🔎 Search by name"}),
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "🔎 Search by name"}),
    )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by Username"}),
    )


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "prax_years",
        )


class CookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["dishes"].initial = self.instance.dishes.all()

    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(), required=False, widget=SelectMultiple
    )

    class Meta:
        model = Cook
        fields = [
            "username",
            "first_name",
            "last_name",
            "prax_years",
            "dishes",
        ]


class DishCreationForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"

    def clean_price(self):
        return validate_price(self.cleaned_data["price"])


def validate_price(price):
    if price < 0:
        raise ValidationError("Price should be a positive value")

    return price


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "🔎 Search by name"}),
    )


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = "__all__"


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"


class ToggleDishToCookDeleteForm(forms.Form):
    class Meta:
        model = Dish
        fields = "__all__"
