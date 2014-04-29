from _curses import flash
import base64
import hashlib
import hmac
import json
import boto
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.shortcuts import render, redirect
from dropbox.client import DropboxOAuth2Flow, DropboxClient


@login_required
def connect_amazon(request):
    """
    Connect Amazon account to user profile
    """
    if request.method == 'POST':
        current_user = request.user
        user_profile = UserProfile.objects.get(user=current_user)
        client_id = request.POST.get('client_id')
        secret_key = request.POST.get('secret_key')
        user_profile.amazon_client_id = client_id
        user_profile.amazon_secret = secret_key
        user_profile.save()

    messages.add_message(request, messages.SUCCESS, 'Successfully linked Amazon credentials')
    # TODO: Redirect to user's file view properly
    return redirect('/dashboard')

@login_required
def amazon_file_view(request):
    """
    Generates the policy and signature for an HTTP POST file upload
    Also makes a connection to AWS S3 with boto and gets a list of all keys in a bucket
    This information is pushed to front end to display files and to handle uploads
    """
    try:
        user = request.user
        profile = UserProfile.objects.get(user=user)
        appid = profile.amazon_client_id
        secretkey = profile.amazon_secret
        conn = boto.connect_s3(appid, secretkey)
        buckets = conn.get_all_buckets()

        # Create policy for HTTP POST and sign it using SHA1 and secret key
        policy = {"expiration": "2112-01-01T00:00:00Z",
                  "conditions": [
                      {"bucket": buckets[0].name},
                      ["starts-with", "$key", ""],
                      {"acl": "private"},
                      {"success_action_redirect": "https://cs242-finalproj.herokuapp.com/dashboard#/service_manager/amazon/files"},
                      ["content-length-range", 0, 5368709120]  # 5GB file size limit in bytes
                  ]
        }
        policy_encoded = base64.b64encode(json.JSONEncoder().encode(policy))
        # Entire process fails for some reason if secretkey is not encoded in ascii or UTF-8
        signature = base64.b64encode(hmac.new(secretkey.encode(encoding='UTF-8'), policy_encoded, hashlib.sha1).digest())

        # Gets all keys of a bucket. Keys in folders will have folder name prepended
        files = buckets[0].get_all_keys()
        files = [f.name for f in files]

        context = {'bucketname': buckets[0].name, 'files': files, 'clientid': appid,
                   'policy': policy_encoded, 'signature': signature}
        return render(request, 'website/amazon/fileview.html', context)
    except:
        messages.add_message(request, messages.ERROR, 'Something went wrong communicating with Amazon S3.')
        return render(request, 'website/amazon/fileview.html')


def get_dropbox_auth_flow(web_app_session):
    redirect_uri = "https://cs242-finalproj.herokuapp.com/service_manager/dropbox/auth_finish"
    return DropboxOAuth2Flow(settings.DROPBOX_KEY, settings.DROPBOX_SECRET, redirect_uri,
                             web_app_session, "dropbox-auth-csrf-token")


def dropbox_auth_start(request):
    """
    Start the dropbox auth flow
    """
    authorize_url = get_dropbox_auth_flow(request.session).start()
    return redirect(authorize_url)


def dropbox_auth_finish(request):
    """
    Finish the dropbox auth flow and save token to userprofile
    """
    try:
        access_token, user_id, url_state = get_dropbox_auth_flow(request.session).finish(request.GET)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.dropbox_token = access_token
        user_profile.save()

        messages.add_message(request, messages.SUCCESS, 'Successfully connected with Dropbox')
        return redirect('/dashboard')
    except DropboxOAuth2Flow.BadRequestException, e:
        return HttpResponseBadRequest()
    except DropboxOAuth2Flow.BadStateException, e:
        # Start the auth flow again.
        return redirect("/service_manager/dropbox/auth_start")
    except DropboxOAuth2Flow.CsrfException, e:
        return HttpResponseForbidden()
    except DropboxOAuth2Flow.NotApprovedException, e:
        flash('Not approved?  Why not, bro?')
        return redirect("/dashboard")
    except DropboxOAuth2Flow.ProviderException, e:
        print "Auth error: %s" % (e,)
        return HttpResponseForbidden()

@login_required
def dropbox_file_view(request):
    """
    The view for files/folders in a dropbox account
    """
    try:
        # user = request.user
        # token = SocialToken.objects.get(account=user, app=1).token  # App = 1 for dropbox, 2 for google
        # if not token:  # Checks for existence of token
        #     messages.add_message(request, messages.ERROR, 'You have not connected with a Dropbox account yet.')
        #     return render('/dashboard')
        #
        # # Initiate a client session
        # client = dropbox.client.DropboxClient(token)
        return render(request, 'website/dropbox/fileview.html')
    except:
        messages.add_message(request, messages.ERROR, 'Error accessing Dropbox files')
        return render(request, 'website/dropbox/fileview.html')


@login_required
def google_file_view(request):
    return render(request, 'website/google/fileview.html')