from django.shortcuts import render

# Create your views here.
from .backend import deadstockfinder

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        size = request.POST.get('size')

        finder = deadstockfinder()
        result = finder.search(name, size)

        return render(request, 'deadstockapp/index.html', {'result': result})

    return render(request, 'deadstockapp/index.html')