import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    user = django_filters.CharFilter(field_name="user__username")

    class Meta:
        model = Message
        fields = ['user', 'created_after', 'created_before']
