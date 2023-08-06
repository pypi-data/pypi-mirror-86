from django.http import StreamingHttpResponse

from .utils import add_query_strings_to_links


class GlobalQueryStringsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Handle image in Content-Type response
        # and handle StreamingHttpResponse response such as large CSV or SVG files.
        if "image" in response["Content-Type"] or isinstance(
            response, StreamingHttpResponse
        ):
            return response

        response.content = add_query_strings_to_links(response.content)
        return response
