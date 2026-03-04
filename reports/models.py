from django.contrib.gis.db import models

class SubCounty(models.Model):
    name = models.CharField(max_length=100)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name

class SpatialReport(models.Model):
    """
    Base class to handle shared spatial logic for different types of reports.
    """
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)
    sub_county_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True  # This ensures Django doesn't create a table for this class

    def perform_spatial_join(self, location):
        """Standardized spatial lookup."""
        match = SubCounty.objects.filter(geom__contains=location).first()
        if match:
            self.sub_county = match
            self.sub_county_name = match.name
        else:
            self.sub_county_name = "Outside Nairobi"

    def save(self, *args, **kwargs):
        if self.location:
            self.perform_spatial_join(self.location)
        super().save(*args, **kwargs)

class PotholeReport(SpatialReport):
    location = models.PointField(srid=4326)
    reporter_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Reported')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='potholes/', null=True, blank=True)

    def __str__(self):
        return f"Pothole at {self.location.x}, {self.location.y}"

class StreetlightReport(SpatialReport):
    location = models.PointField(srid=4326)
    light_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Reported')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='streetlights/', null=True, blank=True)

    def __str__(self):
        return f"Streetlight {self.id} - {self.sub_county_name}"