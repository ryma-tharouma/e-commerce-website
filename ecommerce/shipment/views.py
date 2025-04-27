import json
from venv import logger
from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shipment
from .serializers import ShipmentSerializer
from cart.models import Order,Product

from django.http import JsonResponse
from .utils import create_product_for_delivery
from django.views.decorators.csrf import csrf_exempt
import logging



logger = logging.getLogger(__name__)

def create_product_for_delivery(product, store_id):
    headers = {
        "Authorization": f"TOKEN {settings.STORE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "store_id": store_id,
        "logistical_description": product.description or f"{product.id} No description available",
        # "product_id": product.id  # integer, no str()
        "product_id": f"test_{product.id}"
    }

    print("Request Headers:", headers)
    print("Request Payload:", payload)

    try:
        # response = requests.post(settings.DELIVERY_API_URL, headers=headers, json=payload)
        # print("Response status:", response.status_code)
        # print("Response content:", response.text)
        # response.raise_for_status()
        # return response.json()
        response = requests.post(settings.DELIVERY_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
        response_data = response.json()

        # Assuming the response contains the 'product_id' key
        product_id_delivery = response_data.get('product_id')
        print("Response Data:", response_data)
        # Save the external product ID to the local product's `product_id_delivery` field
        product.product_id_delivery = product_id_delivery
        print("Product ID Delivery:", product.product_id_delivery)
        product.save()

        return response.json()

    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise ValueError(f"{response.status_code} Client Error: {http_err}")
    except Exception as err:
        logger.error(f"Unexpected error occurred: {err}")
        raise ValueError(str(err))


@csrf_exempt
def product_delivery_api(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        logistical_description = data.get('logistical_description') or data.get('description')  # 🔥
        store_id = data.get('store_id')

        if not product_id or not logistical_description or not store_id:
            return JsonResponse({"error": "Missing product_id, logistical_description, or store_id"}, status=400)

        if data.get('get_from_db', False):
            product = Product.objects.get(id=product_id)
        else:
            product = Product(id=product_id, description=logistical_description)

        response_data = create_product_for_delivery(product, store_id)
        return JsonResponse(response_data, status=201)

    except Product.DoesNotExist:
        return JsonResponse({"error": f"Product with ID {product_id} not found"}, status=404)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        logger.exception("Unexpected error in product_delivery_api")
        return JsonResponse({"error": str(e)}, status=500)





@csrf_exempt
def create_product_view(request, product_id):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        store_id = data.get('store_id')

        if not store_id:
            return JsonResponse({"error": "Missing store_id"}, status=400)

        product = Product.objects.get(id=product_id)

        product_data = create_product_for_delivery(product, store_id)
        return JsonResponse({"message": "Product created successfully", "data": product_data}, status=201)

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except ValueError as e:
        logger.error(f"Error in API call 400: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Error in API call: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)




@api_view(['POST'])
def create_shipment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        print(f"Order ID: {order_id}")
        print(f"Request Body: {request.data}")
# 
        # Prepare the payload for the external delivery API
        delivery_payload = {
            "source": request.data.get("source"),
            "destination_text": request.data.get("destination_text"),
            "product_price": str(order.total_price),
            "customer_name": request.data.get("customer_name"),
            "customer_phone": request.data.get("customer_phone"),
            "express": request.data.get("express", False),
            "wilaya": request.data.get("wilaya"),
            "commune": request.data.get("commune"),
            "note_to_driver": request.data.get("note_to_driver", ""),
            "products": [
                {
                    "product_id":item.product.product_id_delivery,  # Use
                    
                    #   str(item.product.id),
                    "quantity": item.quantity
                } for item in order.items.all()
            ]

        }
        for item in order.items.all():
            product_id_delivery =  str(item.product.product_id_delivery)
            print(f"Sending product_id_delivery: {product_id_delivery}")  # Debug log

        headers = {
            "Authorization": f"TOKEN {settings.STORE_TOKEN}",
            "Content-Type": "application/json"
        }

        # Send to external delivery API
        response = requests.post(settings.ORDER_API_URL, json=delivery_payload, headers=headers)

        if response.status_code == 200:
            external_response = response.json()

            # Create local Shipment
            shipment = Shipment.objects.create(
                order=order,
                customer_name=request.data['customer_name'],
                customer_phone=request.data['customer_phone'],
                source=request.data['source'],
                wilaya=request.data['wilaya'],
                commune=request.data['commune'],
                express=request.data.get('express', False),
                note_to_driver=request.data.get('note_to_driver', ''),
                status=request.data.get('status', 'pending'),
                shipment_id=external_response.get('shipment_id')  # adapt based on external API response
            )

            return Response({
                "message": "Shipment created successfully",
                "shipment_id": shipment.shipment_id
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
                "error": "Failed to create shipment with delivery service",
                "details": response.text
            }, status=response.status_code)

    except Order.DoesNotExist:
        print(f"Order with ID {order_id} not found.")
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error in create_shipment: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# @api_view(['POST'])
# def create_shipment(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         print(f"Request Body: {request.data}")
        
#         # Send POST request to the product delivery API to create the product
#         product_delivery_url = f"http://127.0.0.1:8000/api/shipment/product-delivery/{order_id}/"
#         response = requests.post(product_delivery_url, json=request.data)
        
#         if response.status_code == 200:
#             # Automatically extract product_id from the response
#             product_data = response.json()
#             product_id = product_data.get("data", {}).get("id", None)
            
#             if not product_id:
#                 return Response({"error": "Product ID not found in the response"}, status=status.HTTP_400_BAD_REQUEST)

#             # Prepare the payload for the external delivery API
#             delivery_payload = {
#                 "source": request.data.get("source"),
#                 "destination_text": request.data.get("destination_text"),
#                 "product_price": str(order.total_price),
#                 "customer_name": request.data.get("customer_name"),
#                 "customer_phone": request.data.get("customer_phone"),
#                 "express": request.data.get("express", False),
#                 "wilaya": request.data.get("wilaya"),
#                 "commune": request.data.get("commune"),
#                 "note_to_driver": request.data.get("note_to_driver", ""),
#                 "products": [
#                     {
#                         "product_id": product_id,  # Directly use product_id from the response
#                         "quantity": item.quantity
#                     } for item in order.items.all()
#                 ]
#             }

#             # Debug: print each product ID and quantity being sent
#             for item in order.items.all():
#                 print(f"Sending product_id: {product_id} with quantity: {item.quantity}")  # Debug log

#             headers = {
#                 "Authorization": f"TOKEN {settings.STORE_TOKEN}",
#                 "Content-Type": "application/json"
#             }

#             # Send to external delivery API
#             external_response = requests.post(settings.ORDER_API_URL, json=delivery_payload, headers=headers)

#             if external_response.status_code == 200:
#                 external_data = external_response.json()

#                 # Create local Shipment
#                 shipment = Shipment.objects.create(
#                     order=order,
#                     customer_name=request.data['customer_name'],
#                     customer_phone=request.data['customer_phone'],
#                     source=request.data['source'],
#                     wilaya=request.data['wilaya'],
#                     commune=request.data['commune'],
#                     express=request.data.get('express', False),
#                     note_to_driver=request.data.get('note_to_driver', ''),
#                     status=request.data.get('status', 'pending'),
#                     shipment_id=external_data.get('shipment_id')  # adapt based on external API response
#                 )

#                 return Response({
#                     "message": "Shipment created successfully",
#                     "shipment_id": shipment.shipment_id
#                 }, status=status.HTTP_201_CREATED)

#             else:
#                 return Response({
#                     "error": "Failed to create shipment with delivery service",
#                     "details": external_response.text
#                 }, status=external_response.status_code)

#         else:
#             return Response({
#                 "error": "Failed to create product with delivery service",
#                 "details": response.text
#             }, status=response.status_code)

#     except Order.DoesNotExist:
#         return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
