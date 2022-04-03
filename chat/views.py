from django.shortcuts import render, HttpResponseRedirect, reverse


def index(request):
    return HttpResponseRedirect(reverse('chat:chat'))


def chat(request):
    username = request.COOKIES.get('username') or ''
    context = {'username': username}
    return render(request, 'chat/chat.html', context=context)
