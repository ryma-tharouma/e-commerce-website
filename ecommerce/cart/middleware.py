# # middleware.py
# class SessionPersistenceMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Force la création de session si manquante
#         if not request.session.session_key:
#             request.session.create()
#             request.session.save()
#             print(f"🔐 Session créée: {request.session.session_key}")
        
#         response = self.get_response(request)
        
#         # Double vérification du cookie
#         if not request.COOKIES.get('sessionid'):
#             response.set_cookie(
#                 key='sessionid',
#                 value=request.session.session_key,
#                 max_age=60*60*24*14,  # 2 semaines
#                 secure=True,
#                 httponly=True,
#                 samesite='None',
#                 path='/'
#             )
#         return response

# cart/middleware.py
class SessionPersistenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifie les cookies avant la vue
        if not request.COOKIES.get('sessionid'):
            request.session.save()
        
        response = self.get_response(request)
        
        # Force le cookie si manquant
        if hasattr(request, 'session') and request.session.session_key:
            response.set_cookie(
                'sessionid',
                request.session.session_key,
                secure=True,
                httponly=True,
                samesite='None',
                max_age=60*60*24*14  # 2 semaines
            )
        return response