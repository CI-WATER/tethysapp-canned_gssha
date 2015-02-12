from django.shortcuts import render


def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'canned_gssha/home.html', context)