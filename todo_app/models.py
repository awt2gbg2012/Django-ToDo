from django.db import models
from django.contrib import admin

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.encoding import force_text

class DateTime(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.datetime)


class Item(models.Model):
    name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    done = models.BooleanField(default=False)


class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "created", "done"]
    search_fields = ["name"]


class ItemInline(admin.TabularInline):
    model = Item


class DateAdmin(admin.ModelAdmin):
    list_display = ["datetime"]
    inlines = [ItemInline]


    def response_add(self, request, obj, post_url_continue='../%s/',
                     continue_editing_url=None, add_another_url=None,
                     hasperm_url=None, noperm_url=None):
        """
        Determines the HttpResponse for the add_view stage.

        :param request: HttpRequest instance.
        :param obj: Object just added.
        :param post_url_continue: Deprecated/undocumented.
        :param continue_editing_url: URL where user will be redirected after
                                     pressing 'Save and continue editing'.
        :param add_another_url: URL where user will be redirected after
                                pressing 'Save and add another'.
        :param hasperm_url: URL to redirect after a successful object creation
                            when the user has change permissions.
        :param noperm_url: URL to redirect after a successful object creation
                           when the user has no change permissions.
        """
        if post_url_continue != '../%s/':
            warnings.warn("The undocumented 'post_url_continue' argument to "
                          "ModelAdmin.response_add() is deprecated, use the new "
                          "*_url arguments instead.", DeprecationWarning,
                          stacklevel=2)
        opts = obj._meta
        pk_value = obj.pk
        app_label = opts.app_label
        model_name = opts.module_name
        site_name = self.admin_site.name

        msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}

        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if "_continue" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % msg_dict
            self.message_user(request, msg)
            if continue_editing_url is None:
                continue_editing_url = 'admin:%s_%s_change' % (app_label, model_name)
            url = reverse(continue_editing_url, args=(quote(pk_value),),
                          current_app=site_name)
            if "_popup" in request.POST:
                url += "?_popup=1"
            return HttpResponseRedirect(url)

        if "_popup" in request.POST:
            return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script></body></html>' % \
                # escape() calls force_text.
                (escape(pk_value), escapejs(obj)))
        elif "_addanother" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may add another %(name)s below.') % msg_dict
            self.message_user(request, msg)
            if add_another_url is None:
                add_another_url = 'admin:%s_%s_add' % (app_label, model_name)
            url = reverse(add_another_url, current_app=site_name)
            return HttpResponseRedirect(url)
        else:
            msg = _('The %(name)s "%(obj)s" was added successfully.') % msg_dict
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                if hasperm_url is None:
                    hasperm_url = 'admin:%s_%s_changelist' % (app_label, model_name)
                url = reverse(hasperm_url, current_app=site_name)
            else:
                if noperm_url is None:
                    noperm_url = 'admin:index'
                url = reverse(noperm_url, current_app=site_name)
            return HttpResponseRedirect(url)


admin.site.register(Item, ItemAdmin)
admin.site.register(DateTime, DateAdmin)
