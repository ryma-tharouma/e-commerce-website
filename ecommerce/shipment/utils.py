# # shipment/utils.py
# import json
# import logging

# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# from cart.models import Product

# # Configure logging
# logger = logging.getLogger(__name__)


# def create_product_for_delivery(product):
#     """
#     Creates a product entry in the external delivery service.

#     Args:
#         product (Product): The product instance to be created.

#     Returns:
#         dict: The response data from the delivery service.

#     Raises:
#         ValueError: If the product creation fails.
#         Exception: For any other unexpected errors.
#     """
#     url = "https://backend.maystro-delivery.com/api/stores/product/"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {settings.STORE_TOKEN}"
#     }
    
#     data = {
#         "store_id": settings.STORE_ID,
#         "logistical_description": product.description or "No description available",
#         "product_id": str(product.id),
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()  # Raises HTTPError for bad responses
#         logger.info(f"Product {product.id} created successfully.")
#         return response.json()
#     except requests.exceptions.HTTPError as http_err:
#         logger.error(f"HTTP error occurred: {http_err}")
#         raise ValueError(f"Failed to create product: {http_err}") from http_err
#     except requests.exceptions.RequestException as req_err:
#         logger.error(f"Request error occurred: {req_err}")
#         raise ValueError(f"Failed to create product: {req_err}") from req_err
#     except Exception as err:
#         logger.error(f"Unexpected error occurred: {err}")
#         raise Exception(f"An unexpected error occurred: {err}") from err

import requests
from django.conf import settings

def create_product_for_delivery(product):
    DELIVERY_API_URL = getattr(settings, "DELIVERY_API_URL", None)
    STORE_TOKEN = getattr(settings, "STORE_TOKEN", None)

    if not DELIVERY_API_URL or not STORE_TOKEN:
        raise ValueError("Missing DELIVERY_API_URL or STORE_TOKEN in settings")

    headers = {
        "Authorization": f"Bearer {STORE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "store_id": settings.STORE_ID,  # Replace this with your store id
        "logistical_description": product.description,
        "product_id": str(product.id)
    }

    response = requests.post(DELIVERY_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()
