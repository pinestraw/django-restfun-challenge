from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.utils.translation import gettext_lazy as _


def clean_existing_user_values(query_param, instance, validation_class):
    message = _("{value} is already used by another user.")
    error = {
        key: message.format(field=key.capitalize(), value=val)
        for key, val in query_param.items()
    }

    def _error_or_delete():
        if user.is_active:
            raise validation_class(error)
        elif user.pk:
            user.delete()

    try:
        user = User.objects.get(**query_param)
        for key, val in query_param.items():
            field = user._meta.get_field(key).verbose_name
            error = {key: message.format(field=field.capitalize(), value=val)}
    except ObjectDoesNotExist:
        pass
    except MultipleObjectsReturned:
        qs = User.objects.filter(**query_param)

        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)

        if qs.filter(is_active=True).exists():
            raise validation_class(error)
        else:
            qs.filter(is_active=False).delete()
    else:
        if instance:
            if instance.pk != user.pk:
                _error_or_delete()
            return  # no need to delete if it is the same instance
        else:
            _error_or_delete()
