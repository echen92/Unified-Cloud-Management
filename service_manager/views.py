import base64
import hashlib
import hmac
import json
import boto
import dropbox
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialToken, SocialApp


@login_required
def amazon_file_view(request):
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
                      {"success_action_redirect": "http://localhost:8000/dashboard#/service_manager/amazon/files"},
                      # ["starts-with", "$Content-Type", ""],
                      ["content-length-range", 0, 5368709120]  # 5GB file size limit in bytes
                  ]
        }
        policy_encoded = base64.b64encode(json.JSONEncoder().encode(policy))
        # Entire process fails for some reason if secretkey is not encoded in ascii or UTF-8
        signature = base64.b64encode(hmac.new(secretkey.encode(encoding='UTF-8'), policy_encoded, hashlib.sha1).digest())

        files = buckets[0].get_all_keys()
        files = [f.name for f in files]

        context = {'bucketname': buckets[0].name, 'files': files, 'clientid': appid,
                   'policy': policy_encoded, 'signature': signature}
        return render(request, 'website/amazon/fileview.html', context)
    except:
        messages.add_message(request, messages.ERROR, 'Something went wrong communicating with Amazon S3.')

    return render(request, 'website/amazon/fileview.html')


@login_required
def dropbox_upgrade_token(request):
    try:
        user = request.user
        socialtoken = SocialToken.objects.get(account=user, app=1)  # App = 1 for dropbox, 2 for google
        # We need to convert the OAuth1 token to OAuth2, then deauth the old tokens
        # Extract the token from SocialToken object
        token = socialtoken.token
        token_secret = socialtoken.token_secret

        socialapp = SocialApp.objects.get(name='Dropbox')
        APP_KEY = socialapp.client_id
        APP_SECRET = socialapp.secret

        # Get a DropboxClient object using an existing OAuth 1 access token.
        sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET)
        sess.set_token(token, token_secret)
        client = dropbox.client.DropboxClient(sess)

        # Create an OAuth 2 access token for the user.
        oauth2_token = client.create_oauth2_access_token()

        # Disable the OAuth 1 access token.
        client.disable_access_token()
        socialtoken.token = oauth2_token
        socialtoken.save()

        return redirect('/dashboard')

    except:
        print 'SOMETHING WENT WRONG IN UPGRADING TOKEN'
        messages.add_message(request, messages.ERROR, 'Something went wrong while upgrading access token')
        return render(request, 'website/dashboard.html')

@login_required
def dropbox_file_view(request):
    try:
        user = request.user
        token = SocialToken.objects.get(account=user, app=1).token  # App = 1 for dropbox, 2 for google
        if not token:  # Checks for existence of token
            messages.add_message(request, messages.ERROR, 'You have not connected with a Dropbox account yet.')
            return render('/dashboard')

        # Initiate a client session
        client = dropbox.client.DropboxClient(token)
        return render(request, 'website/dashboard.html')
    except:
        print 'SOMETHING WENT WRONG IN DROPBOX FILE VIEW'
        return render(request, 'website/dropbox/fileview.html')


@login_required
def google_file_view(request):
    return render(request, 'website/google/fileview.html')