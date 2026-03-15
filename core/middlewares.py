import threading
 
_request_middleware_thread_local = threading.local()
 
def get_current_request():
    return getattr(_request_middleware_thread_local, "current_request", None)
 
class RequestMiddleware:
    thread_local = _request_middleware_thread_local  # Ensure both use the same object
 
    def __init__(self, get_response):
        self.get_response = get_response
 
    def __call__(self, request):
        self.__class__.thread_local.current_request = request  # Store request in thread-local storage
        response = self.get_response(request)
        return response