from django.db import models

# Create your models here.

class OSMSector(models.Model):
    name = models.CharField(max_length=255, help_text="A descriptive name for this sector.")
    date_time = models.DateTimeField(auto_now_add=True, help_text="The date and time this sector was defined.")
    bbox_upper_left_x = models.FloatField(help_text="Bounding box left side (longitude).")
    bbox_upper_left_y = models.FloatField(help_text="Bounding box lower side (latitude).")
    bbox_lower_right_x = models.FloatField(help_text="Bounding box right side (longitude).")
    bbox_lower_right_y = models.FloatField(help_text="Bounding box upper side (latitude).")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "OSM Sector"
        verbose_name_plural = "OSM Sectors"
