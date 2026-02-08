from social_django.utils import load_strategy, load_backend
from social_core.exceptions import AuthException
from rest_framework_simplejwt.tokens import RefreshToken


def google_authenticate(request, access_token):
    """
    Func for testing google authentication without frontend and redirection
    """

    # Give social_auth context and selecting an external backend for authentication
    strategy = load_strategy(request)

    backend = load_backend(
        strategy=strategy,
        name="google-oauth2",
        redirect_uri=None
    )
    # Check with Google if user is real and create/get his instance
    try:
        user = backend.do_auth(access_token=access_token)
    except AuthException as e:
        raise e

    if not user:
        raise Exception("Authentication failed")

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }