from django.conf import settings

__app_settings = {
    "CREATE_MISSING": True,
    "CREATE_DEFAULT": None,
}


def get_settings(name, default=None):
    name = name.upper()
    user_settings = getattr(settings, "FEATURE_FLAG", {})
    if name in user_settings:
        return user_settings[name]
    return __app_settings.get(name, default)
