from django.contrib.contenttypes.generic import BaseGenericInlineFormSet, generic_inlineformset_factory
from django.forms.formsets import BaseFormSet, formset_factory
from django.forms.models import BaseModelFormSet, BaseInlineFormSet, modelformset_factory, inlineformset_factory
from django.utils.functional import curry


class BaseFormSetFactory:
    """
    A base class for declaritive style formset definitions.
    Used by each of the following:
    * FormSetMixin
    * ModelFormSetMixin
    * InlineFormSetMixin
    * GenericInlineFormSetMixin
    """
    formset_context_name = None

    def get_context_data(self, **kwargs):
        """
        If `inlines_names` has been defined, add each formset to the context
        under its corresponding entry in `inlines_names`.
        """
        if self.formset_context_name and 'formset' in kwargs:
            kwargs[self.formset_context_name] = kwargs['formset']
        return super().get_context_data(**kwargs)

    def formset_factory(self):
        raise NotImplemented('formset_factory() must be implemented')

    def get_extra_form_kwargs(self):
        return {}

    def get_formset(self, data=None, files=None, **kwargs):
        formset_class = self.formset_factory()

        ext_form_kwargs = self.get_extra_form_kwargs()
        if ext_form_kwargs:
            formset_class.form = staticmethod(
                curry(formset_class.form, **ext_form_kwargs))
        return formset_class(data=data, files=files, **kwargs)


class FormsetMixin(BaseFormSetFactory):
    """
    Mixin class for constructing a formset.
    """
    formset_class = BaseFormSet
    form_class = None
    extra = 2
    can_order = False
    can_delete = False
    max_num = None

    def formset_factory(self):
        kwargs = {
            'formset': self.formset_class,
            'extra': self.extra,
            'max_num': self.max_num,
            'can_order': self.can_order,
            'can_delete': self.can_delete
        }
        return formset_factory(self.form_class, **kwargs)


class ModelFormSetMixin(BaseFormSetFactory):
    """
    Mixin class for constructing a model formset.
    """
    formset_class = BaseModelFormSet
    form_class = None
    extra = 2
    can_order = False
    can_delete = False
    max_num = None
    model = None
    fields = None
    exclude = None
    formfield_callback = None

    def formset_factory(self):
        kwargs = {
            'formset': self.formset_class,
            'extra': self.extra,
            'max_num': self.max_num,
            'can_order': self.can_order,
            'can_delete': self.can_delete,
            'fields': self.fields,
            'exclude': self.exclude,
            'formfield_callback': self.formfield_callback
        }
        if self.form_class:
            kwargs['form'] = self.form_class
        return modelformset_factory(self.model, **kwargs)


class InlineFormSetFactory(BaseFormSetFactory):
    """
    Mixin class for constructing an inline formset.
    """
    formset_class = BaseInlineFormSet
    form_class = None
    extra = 2
    can_order = False
    can_delete = False
    max_num = None
    model = None
    fields = None
    exclude = None
    formfield_callback = None
    inline_model = None
    fk_name = None

    def formset_factory(self):
        """
        Returns the keyword arguments for calling the formset factory
        """
        kwargs = {
            'formset': self.formset_class,
            'extra': self.extra,
            'max_num': self.max_num,
            'can_order': self.can_order,
            'can_delete': self.can_delete,
            'fields': self.fields,
            'exclude': self.exclude,
            'formfield_callback': self.formfield_callback,
            'fk_name': self.fk_name
        }
        if self.form_class:
            kwargs['form'] = self.form_class
        return inlineformset_factory(self.model, self.inline_model, **kwargs)


