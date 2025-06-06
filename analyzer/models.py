from django.db import models


class CodeSubmission(models.Model):
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    analysis = models.TextField()

    def __str__(self):
        return f"Submission {self.id}"
