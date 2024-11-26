from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .form import *
# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public_chat')
    chat_messages = chat_group.chat_messages.all()[:30]

    # 保存Message到DB
    form = ChatmessageCreateFrom()

    if request.method == 'POST':
        form = ChatmessageCreateFrom(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            #新message
            context = {
                'message':message,
                'user': request.user
            }

            # 表示不用回傳整個home，回傳這一部分的新message即可
            return render(request, 'partials/chat_message_p.html',context)

    return render(request,'chat.html',{'chat_messages':chat_messages,'form':form})
