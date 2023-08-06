# -*- coding: utf-8 -*-
"""Sync controlpanel view."""

from collective.contentsync import _
from collective.contentsync.sync.sync import full_sync
from collective.contentsync.sync.sync import sync_queue
from plone.app.registry.browser import controlpanel
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.autoform import directives
from plone.supermodel import model
from plone.z3cform import layout
from z3c.form import button
from z3c.form.browser.multi import MultiWidget
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from zope import schema
from zope.interface import implementer
from zope.interface import Interface

import plone.api


DEFAULT_OMITTED_UPDATE_FIELDS = [
]


class ITargetRow(model.Schema):
    id = schema.TextLine(title=_("ID target"))
    title = schema.TextLine(title=_("Title target"))
    url = schema.TextLine(title=_("URL"))
    username = schema.TextLine(title=_("Username"))
    password = schema.TextLine(title=_("Password"))


def context_property(name, default=None):

    def getter(self, default=default):
        return getattr(self.context, name, default)

    def setter(self, value):
        setattr(self.context, name, value)

    def deleter(self):
        delattr(self.context, name)

    return property(getter, setter, deleter)

class ISyncControlPanelForm(Interface):
    """A form to edit synchronization settings."""


class ISyncSettings(model.Schema):
    """Global settings."""

    sync_immediately = schema.Bool(
        description=_(
            u"If activated, a synchronization will be tried right away. If it fails, "
            u"the content item will be added to the queue.",
        ),
        default=False,
        required=False,
        title=_(u"Sync immediately"),
    )

    omitted_update_fields = schema.List(
        default=DEFAULT_OMITTED_UPDATE_FIELDS,
        description=_(
            u"This list contains field names which should be ignored when the remote "
            u"item already exists. Add one item per line."
        ),
        required=False,
        title=_(u"Ignored fields for update"),
        value_type=schema.TextLine(),
    )

#    directives.widget("targets", MultiWidget)
    directives.widget("targets", DataGridFieldFactory)
    targets = schema.List(
        description=_(u"Synchronization targets"),
        required=False,
        title=_(u"Targets"),
        default=[],
        value_type=DictRow(title="row", schema=ITargetRow)
    )

    directives.mode(ISyncControlPanelForm, queue="display")
    queue = schema.Set(
        description=_(
            u"A list of content items which should be synced with next "
            u"synchronization run."
        ),
        required=False,
        title=_(u"Sync Queue"),
        value_type=schema.TextLine(title=_(u"Path")),
    )


@implementer(ISyncControlPanelForm)
class SyncControlPanelForm(controlpanel.RegistryEditForm):
    """Sync control panel form."""

    schema = ISyncSettings
    schema_prefix = "collective.contentsync"
    label = _(u"Content Sync Settings")
    buttons = controlpanel.RegistryEditForm.buttons.copy()
    handlers = controlpanel.RegistryEditForm.handlers.copy()

    targets = context_property('targets')

    def updateActions(self):  # noqa: N802
        super(SyncControlPanelForm, self).updateActions()
        if "run_sync" in self.actions:
            self.actions["run_sync"].addClass("destructive")

    @button.buttonAndHandler(
        _(u"Sync queued items now"),
        name="run_sync",
    )
    def handle_run_sync(self, action):
        sync_queue()
        plone.api.portal.show_message(
            message=_(u"Synchronization run was successful."),
            request=self.request,
        )
        self.request.response.redirect(
            u"{0}/{1}".format(
                plone.api.portal.get().absolute_url(), "@@collective.contentsync-settings"
            )
        )

    @button.buttonAndHandler(
        _(u"Full sync"),
        name="full_sync",
    )
    def handle_full_sync(self, action):
        queue = plone.api.portal.get_registry_record("collective.contentsync.queue")
        queue = queue or set()
        missed = full_sync()
        queue = queue & missed
        plone.api.portal.set_registry_record("collective.contentsync.queue", queue)


SyncControlPanelView = layout.wrap_form(SyncControlPanelForm, ControlPanelFormWrapper)
