from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Django REST Framework'ün default handler'ını çalıştır
    response = exception_handler(exc, context)

    if response is not None:
        # response'u standart formata çevir
        response.data = {
            'success': False,
            'error': response.data,
            'status': response.status_code
        }

    return response