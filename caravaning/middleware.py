from django.utils.cache import patch_cache_control


class HTMLNoStoreMiddleware:
    """
    Evita almacenar documentos HTML durante
    las pruebas de navegación y autenticación.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        content_type = response.get(
            "Content-Type", ""
        ).lower()

        if content_type.startswith("text/html"):
            patch_cache_control(
                response,
                no_store=True,
                private=True,
                max_age=0,
            )

        return response
