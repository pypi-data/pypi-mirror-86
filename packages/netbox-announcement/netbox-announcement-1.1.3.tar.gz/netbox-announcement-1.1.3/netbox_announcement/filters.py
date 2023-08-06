import django_filters
from django.contrib.auth.models import User
from django.db.models import Q

from utilities.filters import BaseFilterSet
from dcim.models import Device, Site
from virtualization.models import VirtualMachine

from .models import Announcement, AnnouncementStatus, AnnouncementEmailPreConfig, AnnouncementUpdate
from .choices import *

class AnnouncementFilterSet(BaseFilterSet):
    """
    Announcement Filter Set
    """
    q = django_filters.CharFilter(
        method = 'search',
        label = 'Search'
    )
    created_at = django_filters.DateTimeFromToRangeFilter()
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user__id',
        queryset=User.objects.all(),
        to_field_name='id',
        label='Author',
    )
    type = django_filters.MultipleChoiceFilter(
        choices=AnnouncementTypeChoices,
        null_value=None
    )
    status = django_filters.ModelMultipleChoiceFilter(
        queryset=AnnouncementStatus.objects.all(),
        field_name='status__id',
        to_field_name='id',
        label='Status',
    )
    related_site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='related_site__id',
        to_field_name='id',
        label='Related Site'
    )
    related_device = django_filters.ModelMultipleChoiceFilter(
        queryset = Device.objects.all(),
        field_name='related_device__id',
        to_field_name='id',
        label='Related Device'
    )
    related_vm = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualMachine.objects.all(),
        field_name='related_vm__id',
        to_field_name='id',
        label='Related VM'
    )
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'subject', 'user', 'type', 'status', 'related_site', 'related_device', 'related_vm', 'mailed'
        ]
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        
        return queryset.filter(
            Q(subject__icontains=value) |
            Q(related_site__name__icontains=value) |
            Q(related_device__name__icontains=value) |
            Q(related_vm__name__icontains=value) |
            Q(user__username__icontains=value) |
            Q(type__icontains=value) |
            Q(status__status__icontains=value)
        )


class AnnouncementStatusFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search'
    )

    class Meta:
        model = AnnouncementStatus
        fields = ['id', 'status', 'status_label']
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(status__icontains=value) |
            Q(status_label__icontains=value)
        )


class AnnouncementEmailPreConfigFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search'
    )
    
    class Meta:
        model = AnnouncementEmailPreConfig
        fields = ['id', 'name']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(name__icontains=value)
        )


class AnnouncementUpdateFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search'
    )
    created_at = django_filters.DateTimeFromToRangeFilter()
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user__id',
        queryset=User.objects.all(),
        to_field_name='id',
        label='Author',
    )
    announcement = django_filters.ModelMultipleChoiceFilter(
        field_name='announcement__id',
        queryset=Announcement.objects.all(),
        to_field_name='id',
        label='Announcement',
    )
    updated_at = django_filters.DateTimeFromToRangeFilter()
    class Meta:
        model = AnnouncementUpdate
        fields = ['id', 'announcement', 'user', 'mailed', 'created_at', 'updated_at','uid']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(announcement__subject__icontains=value) |
            Q(user__username__icontains=value) |
            Q(mailed__icontains=value) |
            Q(uid__icontains=value)
        )
