from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # ใช้ CustomUser

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_chatrooms")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2_chatrooms")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # ป้องกันการสร้างห้องซ้ำระหว่างผู้ใช้สองคน

    def __str__(self):
        return f"ChatRoom between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in ChatRoom {self.chatroom.id}"
