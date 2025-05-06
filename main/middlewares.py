from django.shortcuts import render
from django.utils.timezone import now 


class SiteUnderMaintananceMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    
    def __call__(self,request):
        if request.path.startswith('/admin/') or request.path.startswith('/accounts/'):
            return self.get_response(request)
        return render(request,"main/under_construction.html")


class UserActiveMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    
    def __call__(self,request):
        if request.user.is_authenticated:
            profile=getattr(request.user,'profile',None)
            if profile:
                print(f"Previous last_seen for {request.user.username}: {profile.last_seen}")
                profile.last_seen=now()
                profile.save(update_fields=['last_seen'])
        return self.get_response(request)



