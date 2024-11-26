from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True)

    # 接收self（即 ChatGroup 实例）作为参数。该方法定义了当 ChatGroup 对象被转换为字符串时的行为
    def __str__(self):
        return self.group_name #返回是该chat group的名称

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup,related_name='chat_messages', on_delete=models.CASCADE)  # 所属的聊天组
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True) #auto_now_add=True 表示在创建时会自动设置为当前时间，且不会被修改

    def __str__(self):
        return f"{self.author.username}: {self.body}"

    class Meta:
        ordering = ['-created'] #表示模型查詢結果默認按照created降序排列