from django.contrib import admin

# Register your models here.

from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import OSMSector

@admin.register(OSMSector)
class OSMSectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_time', 'bbox_upper_left_x', 'bbox_upper_left_y', 'bbox_lower_right_x', 'bbox_lower_right_y',)
    
    actions = ['get_osm_data']

    def get_osm_data(self, request, queryset):
        # assuming you're dealing with only one sector at a time
        sector = queryset.first() 
        bbox = f"{sector.bbox_upper_left_x},{sector.bbox_upper_left_y},{sector.bbox_lower_right_x},{sector.bbox_lower_right_y}"

        # assuming you have a URL pattern named 'get_osm' that accepts 'bbox' as a query parameter
        url = reverse('get_osm') + f'?bbox={bbox}' 

        return HttpResponseRedirect(url)
    get_osm_data.short_description = "Get OSM data for selected sector"
