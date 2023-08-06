def is_active(name, obj=None):
    from featureflag.models import FeatureFlag

    flag = FeatureFlag.get(name)
    return flag.is_active(obj)
