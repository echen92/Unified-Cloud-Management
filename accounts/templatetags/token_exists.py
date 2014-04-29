from django import template
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter
from accounts.models import UserProfile

register = template.Library()

@register.filter()
@stringfilter
def token_exists(user, provider):
    """
    Filter to check whether an OAuth token for a service exists under the current user's profile
    """
    try:
        userobj = User.objects.get(username=user)
        if provider == 'dropbox':
            if UserProfile.objects.get(user=userobj).dropbox_token:
                return True
            else:
                return False
        elif provider == 'google':
            pass
        elif provider == 'amazon':
            if UserProfile.objects.get(user=userobj).amazon_client_id or UserProfile.objects.get(user=userobj).amazon_secret:
                return True
            else:
                return False

        return False
    except Exception as e:
        print 'TOKEN_CHECK_FILTER: ', '%s (%s)' % (e.message, type(e))
        return False