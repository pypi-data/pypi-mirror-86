""" Audit models. """

# Django
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

# Models
User = get_user_model()


class BaseModel(models.Model):
    """Audit base model which every models inherit."""

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha de creación"
    )
    created_user = models.CharField(
        max_length=128, editable=False, null=True, verbose_name="creado por"
    )
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name="última fecha de modificación"
    )
    modified_user = models.CharField(
        max_length=128, editable=False, null=True, verbose_name="modificado por"
    )
    is_active = models.BooleanField(default=True, verbose_name="activo")

    def _get_user(self, username):
        """Get user by provide username"""
        try:
            user = User.objects.get(username=username)
            return user.get_full_name() or user.username
        except User.DoesNotExist:
            return username

    def get_created_user(self):
        """Get created user"""
        return self._get_user(self.created_user)

    def get_update_user(self):
        """Get updated user"""
        return self._get_user(self.modified_user)

    class Meta:
        """Meta options."""

        abstract = True


class Trace(models.Model):
    """ Model that stores audit logs according to the rules. """

    class ActionChoices(models.IntegerChoices):
        CREATE = 1, 'Crear'
        EDIT = 2, 'Editar'
        DELETE = 3, 'Eliminar'

    id = models.BigAutoField(primary_key=True)
    action = models.PositiveSmallIntegerField(
        choices=ActionChoices.choices, verbose_name="acción"
    )
    message = models.TextField(verbose_name='mensaje')
    content_type = models.ForeignKey(
        "contenttypes.ContentType", 
        on_delete=models.CASCADE,
        verbose_name='contenido'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='id del objecto'
    )
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='usuario'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='fecha')

    def __str__(self):
        return f"{self.content_object}, {self.get_action_display()}"

    class Meta:
        verbose_name = "Rastro"


class Rule(BaseModel):
    """ Modelo que almacena las reglas de auditoría. """

    content_type = models.OneToOneField(
        "contenttypes.ContentType", on_delete=models.CASCADE, verbose_name="Objeto"
    )
    check_create = models.BooleanField("rastrear creaciones")
    check_edit = models.BooleanField("rastrear modificaciones")
    check_delete = models.BooleanField("rastrear eliminaciones")

    def __str__(self):
        return f"Regla de {str(self.content_type).lower()}"

    class Meta:
        verbose_name = "Regla"
