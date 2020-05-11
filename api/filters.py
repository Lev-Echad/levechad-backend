import django_filters as filters

from client.models import Volunteer, HelpRequest


class VolunteerFilter(filters.FilterSet):
    num_helprequests = filters.NumberFilter(lookup_expr='exact')
    num_helprequests__gt = filters.NumberFilter(method='num_helprequests_gt')
    num_helprequests__lt = filters.NumberFilter(method='num_helprequests_lt')

    def num_helprequests_gt(self, queryset, field_name, value):
        return queryset.filter(num_helprequests__gt=value)

    def num_helprequests_lt(self, queryset, field_name, value):
        return queryset.filter(num_helprequests__lt=value)

    class Meta:
        model = Volunteer
        fields = {
            'id': ['exact'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'tz_number': ['exact', 'icontains'],
            'phone_number': ['exact', 'icontains'],
            'date_of_birth': ['gt', 'lt', 'exact'],
            'age': ['gt', 'lt', 'exact'],
            'gender': ['exact'],
            'city': ['exact', 'in'],
            'neighborhood': ['exact', 'icontains'],
            'city__region': ['exact'],
            'moving_way': ['exact'],
            'week_assignments_capacity': ['exact', 'range'],
            'wanted_assignments': ['exact'],
            'score': ['exact'],
            'created_date': ['gt', 'lt', 'exact'],
            'organization': ['exact', 'in']
        }


class HelpRequestsFilter(filters.FilterSet):
    class Meta:
        model = HelpRequest
        fields = {
            'id': ['exact'],
            'city': ['exact', 'in'],
            'city__region': ['exact', 'in'],
            'status': ['exact', 'in'],
            'type': ['exact', 'in'],
            'helping_volunteer__id': ['exact'],
            'notes': ['icontains'],
            'phone_number': ['exact'],
        }
