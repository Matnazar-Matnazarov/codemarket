# config/middleware.py
from debug_toolbar.middleware import DebugToolbarMiddleware


class AdminDebugToolbarMiddleware(DebugToolbarMiddleware):
    def __call__(self, request):
        if request.user.is_staff:
            return super().__call__(request)
        return self.get_response(request)
