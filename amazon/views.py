import boto
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.shortcuts import render, redirect

@login_required
def file_view(request):
    try:
        user = request.user
        profile = UserProfile.objects.get(user=user)
        # appid = profile.amazon_client_id
        # secretkey = profile.amazon_secret
        conn = boto.connect_s3('AKIAJ5DXVRD32MZQFNAA', 'LTtALQjgr0RmKBWiGt95Pcv3TK9x91rh2HzIh3xv')
        buckets = conn.get_all_buckets()

        files = buckets[0].get_all_keys()
        files = [f.name for f in files]

        # print [f.encode('ascii') for f in files]
        folders = [b.name for b in buckets]

        context = {'folders': folders, 'files': files}
        return render(request, 'website/amazon/fileview.html', context)
    except:
        print 'AMAZON CONNECTION FAILED'
    return render(request, 'website/amazon/fileview.html')