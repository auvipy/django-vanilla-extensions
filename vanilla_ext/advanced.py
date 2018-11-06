from django.forms.formsets import all_valid
from django.http import HttpResponseRedirect
from vanilla import GenericModelView
from vanilla_ext import InlineFormSetFactory


class BaseInlinesView(GenericModelView):
    """
     A view class that provides way to multiple inline formsets in a request.

     * CreateWithInlinesView
     * UpdateWithInlinesView

    """
    inlines = []
    inline_context_names = []
    template_name_suffix = '_form'
    success_url = None

    def get_context_data(self, **kwargs):
        """
        If `inlines_names` has been defined, add each formset to the context
        under its corresponding entry in `inlines_names`.
        """
        if self.inline_context_names and 'inlines' in kwargs:
            kwargs.update(zip(self.inline_context_names, kwargs['inlines']))
        return super().get_context_data(**kwargs)

    def get_inlines(self, data=None, files=None, **kwargs):
        """
        Returns the inline formset instances.
        """
        instance = kwargs.get('instance', None)
        inline_formsets = []
        for inline_class in self.inlines:
            inline_instance = inline_class(self.model)
            inline_formset = inline_instance.get_formset(
                data=data, files=files, **kwargs)
            inline_formsets.append(inline_formset)
        return inline_formsets

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid,
        save the associated models and redirect.
        """
        self.object = form.save()
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, inlines):
        """
        If the form or formsets are invalid, re-render the context
        data with the data-filled form and formsets and errors.
        """
        context = self.get_context_data(form=form, inlines=inlines)
        return self.render_to_response(context)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.request.get_full_path()
