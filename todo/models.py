from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

# 👇 Added custom QuerySet
class TodoQuerySet(models.QuerySet):
    def overdue(self):
        now = timezone.now()
        return self.filter(is_completed=False, due_date__lt=now)

# 👇 Added custom Manager
class TodoManager(models.Manager):
    def get_queryset(self):
        return TodoQuerySet(self.model, using=self._db)

    def overdue(self):
        return self.get_queryset().overdue()

class Todo(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        blank=True,
        null=True
    )
    reaction = models.CharField(max_length=5, null=True, blank=True)

    # 👇 Use the new manager
    objects = TodoManager()

    def __str__(self):
        return self.title

    # 👇 Added is_overdue property
    @property
    def is_overdue(self):
        """
        Returns True if:
        - the task is NOT completed
        - the due_date is in the past (timezone-aware)
        """
        if self.is_completed or not self.due_date:
            return False
        now = timezone.now()

        # If due_date is naive (no timezone), assume default tz
        due = self.due_date
        if timezone.is_naive(due):
            due = timezone.make_aware(due, timezone.get_default_timezone())

        return due < now
