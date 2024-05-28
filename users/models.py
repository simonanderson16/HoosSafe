from django.db import models
from django.utils import timezone


class CustomUser(models.Model):
    email = models.EmailField(primary_key=True)
    is_site_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Report(models.Model):
    STATUS_CHOICES = [
        (0, 'New'),
        (1, 'In Progress'),
        (2, 'Resolved'),
        # Add more statuses as needed
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    pub_date_report = models.DateTimeField("date published", default=timezone.now)
    title = models.CharField(max_length=50, default=" ")
    # file = models.FileField(upload_to='static', null=True, blank=True)
    location = models.CharField(max_length=300, default=" ")
    date = models.CharField(max_length=200, default=" ")
    time = models.CharField(max_length=200, default=" ")
    type_of_violation = models.CharField(max_length=300, default="")
    explain = models.TextField(default=" ")
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    note = models.TextField(default="")

    def get_status_display(self):
        return dict(Report.STATUS_CHOICES).get(self.status, 'Unknown')

    # image = models.ImageField(upload_to = 'images', null = True, blank = True)

    def __str__(self):
        user = self.user.email if self.user else "Anonymous"
        return user + " " + str(self.pub_date_report)


class ReportFile(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='static', null=True, blank=True)

    def __str__(self):
        return f"File for Report {self.report.id}"

    def delete(self, using=None, keep_parents=False):
        if self.file:
            self.file.delete(save=False)
        super(ReportFile, self).delete(using=using, keep_parents=keep_parents)