


def check_token(backend, user, response, *args, **kwargs):
    provider = backend.name
    social = user.social.get(provider=provider)
    print(user.social_auth.get(provider='google-oauth2').extra_data['access_token'])