def MainFeed(request):
    posts = Post.objects.all()
    data = serializers.serialize('json', posts)
    return JsonResponse({'posts': data})


def GetUser(request, user_id):
    user = User.objects.get(username=user_id)
    data = serializers.serialize('json', [user])
    print(user)
    return JsonResponse({'user': data})
    # return JsonResponse({'user': data})
