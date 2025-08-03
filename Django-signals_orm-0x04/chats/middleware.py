import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Deny access if current time is between 21 (9 PM) and 6 AM
        if current_hour >= 21 or current_hour < 6:
            return HttpResponseForbidden("Access to the messaging app is restricted between 9 PM and 6 AM.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = {}  # {ip: [(timestamp1), (timestamp2), ...]}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 1 minute window
            limit = 5

            timestamps = self.message_counts.get(ip, [])
            # Remove timestamps older than 1 minute
            timestamps = [t for t in timestamps if now - t < window]

            if len(timestamps) >= limit:
                return JsonResponse({"error": "Message limit exceeded. Please wait before sending more."}, status=429)

            timestamps.append(now)
            self.message_counts[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and has a role attribute
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return JsonResponse({"error": "Authentication required."}, status=401)

        # Only allow if role is admin or moderator
        if getattr(user, 'role', None) not in ['admin', 'moderator']:
            return JsonResponse({"error": "You do not have permission to perform this action."}, status=403)

        return self.get_response(request)