from django.db import models
from django.contrib.auth.models import User  
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', default = 'profile_photos/default-profile.png'
)
    phone = models.CharField(max_length=15, unique=True, default=None)
    background_photo = models.ImageField(upload_to='background_photos/', blank=True, null=True)
    profile_headline = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.full_name


class LicenseCertificate(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='licenses_certificates')
    name = models.CharField(max_length=255)
    issuing_org = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.userprofile.full_name}"


class Skill(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.skill_name} - {self.userprofile.full_name}"


class Experience(models.Model):

    userprofile = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255) 
    employment_type = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=255)
    is_current = models.BooleanField(default=False)  
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True) 
    location_type = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company} - {self.userprofile.full_name}"

    def duration(self):
        """Returns duration as 'X yrs Y mos'"""
        end = self.end_date or date.today()
        total_months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        years = total_months // 12
        months = total_months % 12
        result = []
        if years > 0:
            result.append(f"{years} yr{'s' if years > 1 else ''}")
        if months > 0:
            result.append(f"{months} mo{'s' if months > 1 else ''}")
        return ' '.join(result) if result else "0 mo"

class Education(models.Model):
    userprofile = models.ForeignKey(
        "UserProfile", 
        on_delete=models.CASCADE, 
        related_name="educations"
    )
    school = models.CharField(max_length=255)  # e.g. Boston University
    degree = models.CharField(max_length=255, blank=True, null=True)  # e.g. Bachelor's
    field_of_study = models.CharField(max_length=255, blank=True, null=True)  # e.g. Business
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # can be null if ongoing
    grade = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.school} ({self.degree or 'No degree'}) - {self.userprofile.full_name}"

class ConnectionRequest(models.Model):
    sender = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')  # prevent duplicate requests

    def __str__(self):
        return f"{self.sender} → {self.receiver} | Accepted: {self.is_accepted}"


class Connection(models.Model):
    user1 = models.ForeignKey(User, related_name="connections_initiated", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="connections_received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"



