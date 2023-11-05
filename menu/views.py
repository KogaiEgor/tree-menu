from django.shortcuts import render

def menu_view(request):
    menu_url = request.build_absolute_uri()
    context = {
        'current_url': menu_url,
    }

    return render(request, 'menu.html', context)
