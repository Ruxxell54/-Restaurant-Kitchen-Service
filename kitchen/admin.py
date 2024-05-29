from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from kitchen.models import Ingredient, DishType, Cook, Dish


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("prax_years",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("prax_years",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                        "prax_years",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name", "cooks",)
    list_filter = ("name", "price", "cooks", "ingredients",)
