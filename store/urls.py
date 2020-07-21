from django.urls import path

from .views import *

urlpatterns = [
    path('', category, name='store'),
    path('adminpanel/', adminpanel, name='adminpanel'),

    path('updateItem/', updateItem, name='updateItem'),
    path('checkout/', checkout, name='checkout'),
    path('processOrder/', processOrder, name='processOrder'),
    path('search/', searchCategory, name='searchCategory'),

    path('subcategory/<int:category_id>/', subcategory, name='subcategory'),
    path('subcategory/products/<int:subcategory_id>/', products, name='products'),
    path('subcategory/products/<int:subcategory_id>/product/<int:product_id>/', current_product, name='current_product'),

    path('contact/', contact_info, name='contact_info'),
    path('delivery/', delivery_info, name='delivery_info'),
    path('oplata/', oplata_info, name='oplata_info'),
    path('feedback/', feedback_info, name='feedback_info'),

    path('pay/', PayView.as_view(), name='pay_view'),
    path('pay-callback/', PayView.PayCallbackView.as_view(), name='pay_callback'),
]