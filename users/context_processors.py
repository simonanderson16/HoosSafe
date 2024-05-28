from django.contrib.auth import get_user
from allauth.socialaccount.models import SocialAccount
from users.views import is_site_admin


def user_info(request):
    user = get_user(request)

    if user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=user).first()
        more_data = social_account.extra_data if social_account else {}

        user_full_name = more_data.get("name", "")
        user_account_name = user.username
        user_email = more_data.get("email", "")
        user_picture = more_data.get("picture", "")
        user_is_site_admin = is_site_admin(user_email) if user_email else False

        if social_account:
            user_account_name = social_account.user.username

        return {
            "user_full_name": user_full_name,
            "user_account_name": user_account_name,
            "user_email": user_email,
            "user_picture": user_picture,
            "user_is_site_admin": user_is_site_admin,
        }
    else:
        return {}
