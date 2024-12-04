from django.db import models
from api.cases.models import Cases
from api.users.models import Clients, Lawyers, Users
from api.common.utils import generate_unique_id

class Conversations(models.Model):
    conversation_id = models.CharField(primary_key=True, default=generate_unique_id, editable=False, max_length=8, unique=True)
    case_id = models.OneToOneField(Cases, on_delete=models.CASCADE, related_name="conversations_case")
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="conversations_client")
    lawyer_id = models.ForeignKey(Lawyers, on_delete=models.CASCADE, related_name="conversations_lawyer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation for Case {self.case.id}"

class Messages(models.Model):
    message_id = models.CharField(primary_key=True, default=generate_unique_id, editable=False, max_length=8, unique=True)
    conversation_id = models.ForeignKey(Conversations, on_delete=models.CASCADE, related_name="messages")
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="messages")
    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message in Conversation {self.conversation.id} by User {self.user.id}"
