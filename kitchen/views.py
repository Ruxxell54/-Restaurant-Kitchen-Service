from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView, PasswordContextMixin)
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.generic import TemplateView
from django.utils.translation import gettext as _

from kitchen.forms import (UserLoginForm,
                           UserPasswordResetForm,
                           RegistrationForm,
                           UserPasswordChangeForm,
                           UserSetPasswordForm,
                           IngredientSearchForm,
                           CookSearchForm,
                           CookCreationForm,
                           CookForm,
                           DishSearchForm,
                           DishCreationForm,
                           ToggleDishToCookDeleteForm)
from kitchen.models import Ingredient, DishType, Cook, Dish
from kitchen_service import settings


@login_required
def index(request):
    """View function for the home page of the site."""
    num_ingredients = Ingredient.objects.count()
    num_dish_types = DishType.objects.count()
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_ingredients": num_ingredients,
        "num_dish_types": num_dish_types,
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "ingredient_list"
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(initial={"name": name})
        context["search_text"] = name
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(initial={"name": name})
        context["search_text"] = name
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "kitchen/dish_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(initial={"username": username})
        context["search_text"] = username
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookForm
    success_url = reverse_lazy("kitchen:cook-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        cook_instance = form.instance
        dishes = form.cleaned_data['dishes']
        cook_instance.dishes.clear()
        for dish in dishes:
            cook_instance.dishes.add(dish)
        return response


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        context["search_text"] = name
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    form_class = DishCreationForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    template_name = "kitchen/dish_form.html"
    form_class = DishCreationForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class UserLoginView(LoginView):
    template_name = "accounts/sign-in.html"
    form_class = UserLoginForm


def logout_view(request):
    logout(request)
    return redirect('/accounts/login')


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = UserPasswordResetForm


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_done.html"
    title = _("Password reset sent")


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
