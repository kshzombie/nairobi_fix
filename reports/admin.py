from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import PotholeReport, StreetlightReport, SubCounty

@admin.register(SubCounty)
class SubCountyAdmin(gis_admin.GISModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PotholeReport)
class PotholeAdmin(gis_admin.GISModelAdmin):
    # Matches your model fields: id, reporter_name, severity, status, created_at
    list_display = ('id', 'reporter_name', 'sub_county_name', 'severity', 'status', 'created_at')
    list_filter = ('status', 'severity', 'sub_county_name')
    search_fields = ('reporter_name', 'sub_county_name')

@admin.register(StreetlightReport)
class StreetlightAdmin(gis_admin.GISModelAdmin):
    # Matches your model fields: id, light_type, status, sub_county_name
    # Note: 'created_at' isn't in your Streetlight model yet, so we use id
    list_display = ('id', 'light_type', 'sub_county_name', 'status')
    list_filter = ('status', 'light_type')
