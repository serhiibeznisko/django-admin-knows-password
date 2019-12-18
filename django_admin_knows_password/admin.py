from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.db import transaction, router
from django.template.response import TemplateResponse
from functools import update_wrapper

from .forms import ChangePasswordForm


class ChangePasswordAdmin(admin.ModelAdmin):
    change_form_template = 'django_admin_knows_password/change_form.html'

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        extra_url = [
            path('<path:object_id>/password_change/', wrap(self.password_change_view), name='%s_%s_password_change' % info),
        ]

        return extra_url + super().get_urls()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(show_change_password_tool=True)
        return self.changeform_view(request, object_id, form_url, extra_context)

    @admin.options.csrf_protect_m
    def password_change_view(self, request, object_id, extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._password_change_view(request, object_id, extra_context)

    def _password_change_view(self, request, object_id, extra_context):
        model = self.model
        opts = model._meta
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, model._meta, object_id)

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        form = ChangePasswordForm()
        if request.POST:
            form = ChangePasswordForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return self.response_change(request, obj)

        fieldsets = [(None, {'fields': form.base_fields})]
        admin_form = helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': 'Change password',
            'adminform': admin_form,
            'opts': opts,
            'app_label': opts.app_label,
            'object': obj,
            **(extra_context or {}),
        }
        return TemplateResponse(request, 'django_admin_knows_password/change_user_password.html', context)
