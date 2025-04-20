
from django.contrib import admin
from .models import CombinatorialAuction, CombinatorialBid, Product
from .forms import CombinatorialBidForm  # import your form

class ProductInline(admin.TabularInline):
    """Permet d'afficher/modifier les produits dans l'admin d'une enchère."""
    model = CombinatorialAuction.products.through  # Relation ManyToMany
    extra = 1  # Nombre de lignes vides à afficher

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(CombinatorialAuction)
class CombinatorialAuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "end_time", "display_products", "Winning_price", "display_Winners")
    list_filter = ("end_time",)
    search_fields = ("id",)
    inlines = [ProductInline]

    def display_products(self, obj):
        """Affiche les noms des produits liés à l'enchère."""
        return ", ".join([p.name for p in obj.products.all()])
    display_products.short_description = "Produits"

    def display_Winners(self, obj):
        """Affiche les noms des winners liés à l'enchère."""
        return ", ".join([p.username for p in obj.Winner_list.all()])
    display_Winners.short_description = "Winners"

@admin.register(CombinatorialBid)
class CombinatorialBidAdmin(admin.ModelAdmin):
    form = CombinatorialBidForm   # <<< ADD your form here
    list_display = ("user", "auction", "display_products", "amount")
    list_filter = ("auction",)
    search_fields = ("user__username",)

    def display_products(self, obj):
        """Affiche les noms des produits liés au bid."""
        return ", ".join([p.name for p in obj.products.all()])
    display_products.short_description = "Produits"
