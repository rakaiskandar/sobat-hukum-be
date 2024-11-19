from django.db import models
from cases.models import Cases
from users.models import Clients, Lawyers, Users

class Conversations(models.Model):
    case = models.OneToOneField(Cases, on_delete=models.CASCADE, related_name="conversations_case")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="conversations_client")
    lawyer = models.ForeignKey(Lawyers, on_delete=models.CASCADE, related_name="conversations_lawyer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation for Case {self.case.id}"

class Messages(models.Model):
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="messages")
    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message in Conversation {self.conversation.id} by User {self.user.id}"
