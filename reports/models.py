from django.contrib.gis.db import models

class SubCounty(models.Model):
    name = models.CharField(max_length=100)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name

class PotholeReport(models.Model):
    # Core Fields
    location = models.PointField(srid=4326)
    reporter_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Reported')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW: Image field for photo capture
    image = models.ImageField(upload_to='potholes/', null=True, blank=True)

    # Spatial Join Fields
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)
    sub_county_name = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automated Administrative Spatial Join (ST_Contains logic)
        if self.location:
            match = SubCounty.objects.filter(geom__contains=self.location).first()
            if match:
                self.sub_county = match
                self.sub_county_name = match.name
            else:
                self.sub_county_name = "Outside Nairobi"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pothole at {self.location.x}, {self.location.y}"


class StreetlightReport(models.Model):
    # Core Fields
    location = models.PointField(srid=4326)
    light_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Reported')
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW: Image field for photo capture
    image = models.ImageField(upload_to='streetlights/', null=True, blank=True)

    # Spatial Join Fields
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)
    sub_county_name = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automated Administrative Spatial Join (ST_Contains logic)
        if self.location:
            match = SubCounty.objects.filter(geom__contains=self.location).first()
            if match:
                self.sub_county = match
                self.sub_county_name = match.name
            else:
                self.sub_county_name = "Outside Nairobi"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Streetlight {self.id} - {self.sub_county_name}"
