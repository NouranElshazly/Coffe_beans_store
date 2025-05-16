from django.shortcuts import render

 


from django.shortcuts import render
from menu.models import MenuItem


def home_view(request):
    # Get best sellers (marked as is_best_seller=True)
    best_sellers = MenuItem.objects.filter(is_best_seller=True)[:2]
    
    # Get popular items (you might want to add a 'popular' field or use some logic)
    popular_items = MenuItem.objects.all().order_by('-created_at')[:8]
    
    context = {
        'best_sellers': best_sellers,
        'popular_items': popular_items,
    }
    return render(request, 'home.html', context)