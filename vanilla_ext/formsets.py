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
