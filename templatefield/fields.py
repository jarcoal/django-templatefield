from django.utils import six
from django.template.loader import get_template_from_string
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import Template, TemplateSyntaxError, defaulttags, loader_tags
from django.core.exceptions import ValidationError

# these tags are considered unsafe and can be disabled as a group
UNSAFE_TAGS = (
    defaulttags.DebugNode,
    loader_tags.ExtendsNode,
    loader_tags.IncludeNode,
    defaulttags.CsrfTokenNode,
    defaulttags.LoadNode,
    loader_tags.BlockNode,
    defaulttags.URLNode,
)

class TemplateField(six.with_metaclass(models.SubfieldBase, models.TextField)):
    """
    A field that stores a Django template.
    """

    _errors = {
        'invalid': _('template contains invalid syntax.'),
        'not_allowed': _('template tag not allowed: %s'),
    }

    def __init__(self, allow_unsafe_tags=False, **kwargs):
        self.allow_unsafe_tags = allow_unsafe_tags
        super(TemplateField, self).__init__(**kwargs)

    def validate(self, value, model_instance):
        super(TemplateField, self).validate(value, model_instance)

        if not self.allow_unsafe_tags:
            for node in value.nodelist:
                if isinstance(node, UNSAFE_TAGS):
                    raise ValidationError(self._errors['not_allowed'] % node)

    def get_default(self):
        """defaults can be specified as a string or a django template obj"""

        if self.has_default():
            default = self.default

            if callable(default):
                default = default()

            if isinstance(default, six.string_types):
                return get_template_from_string(default)

            if isinstance(default, Template):
                return default

        return super(TemplateField, self).get_default()

    def to_python(self, value):
        """convert to template object"""

        if isinstance(value, six.string_types):
            try:
                return get_template_from_string(value)
            except TemplateSyntaxError:
                raise ValidationError(self._errors['invalid'])

        return value

    def get_prep_value(self, value):
        """prepare template for the database"""

        if value is None:
            if not self.null and self.blank:
                return ""
            return None

        return value.origin.source

    def value_to_string(self, value):
        return self.get_prep_value(self._get_val_from_obj(value))
