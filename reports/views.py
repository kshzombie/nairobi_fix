import json
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import PotholeReport, StreetlightReport, SubCounty

def report_issue(request):
    """View to handle Pothole Report submissions with Photo Capture and Spatial Join."""
    if request.method == 'POST':
        severity = request.POST.get('severity')
        description = request.POST.get('description')
        reporter_name = request.POST.get('reporter_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # NEW: Capture the uploaded photo from request.FILES
        image_file = request.FILES.get('image')

        if latitude and longitude:
            pnt = Point(float(longitude), float(latitude), srid=4326)

            # 1. SPATIAL DUPLICATION CHECK (10 meters)
            duplicate_reports = PotholeReport.objects.filter(
                location__distance_lte=(pnt, D(m=10))
            ).exclude(status='Fixed')

            if duplicate_reports.exists():
                return render(request, 'reports/report.html', {
                    'error': f'A similar pothole report already exists within 10 meters.',
                    'severity_val': severity,
                    'description_val': description,
                    'reporter_name_val': reporter_name,
                })

            # 2. SAVE TO DATABASE (The model's save() method handles the Spatial Join)
            PotholeReport.objects.create(
                severity=severity,
                description=description,
                reporter_name=reporter_name,
                location=pnt,
                image=image_file # Physically saves the file to media/potholes/
            )
            return redirect('report_success')

        return render(request, 'reports/report.html', {'error': 'Geolocation failed.'})

    return render(request, 'reports/report.html')


def streetlight_report_issue(request):
    """View to handle Streetlight Report submissions with Photo Capture and Spatial Join."""
    if request.method == 'POST':
        light_type = request.POST.get('light_type')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # NEW: Capture the uploaded photo from request.FILES
        image_file = request.FILES.get('image')

        if latitude and longitude:
            pnt = Point(float(longitude), float(latitude), srid=4326)

            # 1. SPATIAL DUPLICATION CHECK
            duplicate_reports = StreetlightReport.objects.filter(
                location__distance_lte=(pnt, D(m=10))
            ).exclude(status='Repaired')

            if duplicate_reports.exists():
                return render(request, 'reports/streetlight_report.html', {
                    'error': 'A similar streetlight report already exists within 10 meters.',
                    'light_type_val': light_type,
                })

            # 2. SAVE TO DATABASE
            StreetlightReport.objects.create(
                light_type=light_type,
                location=pnt,
                image=image_file # Physically saves the file to media/streetlights/
            )
            return redirect('report_success')

        return render(request, 'reports/streetlight_report.html', {'error': 'Geolocation failed.'})

    return render(request, 'reports/streetlight_report.html')


# --- API ENDPOINTS FOR THE MAP ---

def pothole_data(request):
    """API endpoint serving pothole GeoJSON including the image path."""
    qs = PotholeReport.objects.all()
    geojson_data = serialize('geojson', qs,
        geometry_field='location',
        fields=('severity', 'status', 'sub_county_name', 'description', 'image')
    )
    return JsonResponse(json.loads(geojson_data), safe=False)

def streetlight_data(request):
    """API endpoint serving streetlight GeoJSON including the image path."""
    qs = StreetlightReport.objects.all()
    geojson_data = serialize('geojson', qs,
        geometry_field='location',
        fields=('light_type', 'status', 'sub_county_name', 'image')
    )
    return JsonResponse(json.loads(geojson_data), safe=False)

def subcounty_data(request):
    """API endpoint to serve Nairobi Sub-County boundaries."""
    qs = SubCounty.objects.all()
    geojson_str = serialize('geojson', qs, geometry_field='geom')
    return JsonResponse(json.loads(geojson_str), safe=False)

# --- General Views ---

def dashboard(request):
    return render(request, 'reports/dashboard.html')

def report_success(request):
    return render(request, 'reports/success.html')
