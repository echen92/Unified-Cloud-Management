import base64
import hashlib
import hmac
import json
import boto
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.shortcuts import render, redirect


@login_required
def file_view(request):
    try:
        user = request.user
        profile = UserProfile.objects.get(user=user)
        appid = profile.amazon_client_id
        secretkey = profile.amazon_secret
        conn = boto.connect_s3('AKIAJ5DXVRD32MZQFNAA', 'LTtALQjgr0RmKBWiGt95Pcv3TK9x91rh2HzIh3xv')
        buckets = conn.get_all_buckets()

        policy = {"expiration": "2112-01-01T00:00:00Z",
                  "conditions": [
                      # {"AWSAccessKeyId": appid},
                      {"bucket": buckets[0].name},
                      ["starts-with", "$key", ""],
                      {"acl": "private"},
                      {"success_action_redirect": "http://localhost:8000/dashboard#/amazon/files"},
                      # ["starts-with", "$Content-Type", ""],
                      ["content-length-range", 0, 5368709120]  # 5GB file size limit in bytes
                  ]
        }
        policy_encoded = base64.b64encode(json.JSONEncoder().encode(policy))
        signature = base64.b64encode(hmac.new(secretkey.encode(encoding='ascii'), policy_encoded, hashlib.sha1).digest())

        files = buckets[0].get_all_keys()
        files = [f.name for f in files]
        # print 'GET HERE'

        # print [f.encode('ascii') for f in files]
        # folders = [b.name for b in buckets]

        # context = {}
        context = {'bucketname': buckets[0].name, 'files': files, 'clientid': appid,
                   'policy': policy_encoded, 'signature': signature}
        return render(request, 'website/amazon/fileview.html', context)
    except:
        print 'AMAZON CONNECTION FAILED'
    return render(request, 'website/amazon/fileview.html')
