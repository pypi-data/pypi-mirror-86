""" Audit signals """

# Python
import json
from datetime import datetime

# Django
from django.forms.models import model_to_dict
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

# Middleware
from .middleware import TracingMiddleware

# Models
from .models import Trace, Rule, BaseModel


""" Util function """


def get_diff(instance, created):
    def prepare_dict(dict):
        for key in dict:
            dict[key] = tuple(dict[key]) if isinstance(dict[key], list) else dict[key]
        return dict

    presave = prepare_dict(TracingMiddleware.get_data())
    postsave = prepare_dict(model_to_dict(instance))

    diff = {key: value for key, value in presave.items() - postsave.items()}

    diff = postsave if created else diff
    return diff


"""Signals for reload rules"""


@receiver(post_save, sender=Rule)
def save_rule(sender, **kwargs):
    TracingMiddleware.reload_rules()


@receiver(post_delete, sender=Rule)
def delete_rule(sender, **kwargs):
    TracingMiddleware.reload_rules()


""" Signal for presave instance """


@receiver(pre_save)
def presave_log(sender, instance, **kwargs):
    try:
        presave = sender.objects.get(pk=instance.pk)
        data = model_to_dict(presave)
    except sender.DoesNotExist:
        data = {}
    TracingMiddleware.set_data(data)


""" Signal for postsave instance """


@receiver(post_save)
def save_log(sender, instance, created, **kwargs):
    rule = TracingMiddleware.get_rule_by_classname(sender._meta.model_name)
    if not rule:
        return

    diff = get_diff(instance, created)
    if not diff:
        return

    if created and rule.get("check_create"):
        message = {"creado": diff}
        options = {"action": Trace.ActionChoices.CREATE}
    elif not created and rule.get("check_edit"):
        message = {"editado": diff}
        options = {"action": Trace.ActionChoices.EDIT}
    else:
        return

    options.update(
        {
            "content_object": instance,
            "user": TracingMiddleware.get_user(),
            "message": json.dumps(message),
        }
    )
    Trace.objects.create(**options)


""" Signal for post_delete instance """


@receiver(post_delete)
def save_delete(sender, instance, **kwargs):
    rule = TracingMiddleware.get_rule_by_classname(sender._meta.model_name)

    if not rule:
        return

    if rule.get("check_delete"):
        message = {"eliminado": {}}
        options = {
            "action": Trace.ActionChoices.CREATE,
            "content_object": instance,
            "user": TracingMiddleware.get_user(),
            "message": json.dumps(message),
        }
        Trace.objects.create(**options)


""" """


@receiver(post_save)
def save_user_in_base_model(sender, instance, created, **kwargs):
    """Save audit fields"""
    if not issubclass(sender, BaseModel):
        return

    # Disconect signals
    pre_save.disconnect(presave_log)
    post_save.disconnect(save_log)
    post_save.disconnect(save_user_in_base_model)

    # Update user
    user = TracingMiddleware.get_user()
    user = user.username if user else "root"
    if created:
        instance.created_user = user
    instance.modified_user = user
    instance.save()

    # Reconnect sigals
    post_save.connect(save_user_in_base_model)
    post_save.connect(save_log)
    pre_save.connect(presave_log)
