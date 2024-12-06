from django.db import models
import uuid

class FileTask(models.Model):
    task_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    file_name = models.CharField(max_length=255)
    file_content = models.TextField()
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('error', 'Error')
        ],
        default='processing'
    )
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.file_name} - {self.status}"
