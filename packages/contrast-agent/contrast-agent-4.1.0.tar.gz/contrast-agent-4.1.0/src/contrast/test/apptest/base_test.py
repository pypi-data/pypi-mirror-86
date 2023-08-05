# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import importlib
import os
import pickle
import sys
import subprocess

import mock
from webtest import TestApp

from contrast.agent.policy import patch_manager
from contrast.agent.assess.utils import clear_properties
from contrast.agent.request_context import RequestContext
from contrast.test.settings_builder import SettingsBuilder

SETTINGS_STATE_PATCH_LOC = "contrast.agent.middlewares.base_middleware.SettingsState"


class BaseContrastTest(object):
    @property
    def application_module_name(self):
        """
        The WSGI application module name, as a string.

        Example:
        ```
        # file: app/wsgi.py
        application = create_wsgi_application()
        ```

        Here, the `application` WSGI callable is defined in the app.wsgi module
        at app/wsgi.py. This means application_module_name should be "app.wsgi".
        """
        raise NotImplementedError

    @property
    def application_attribute_name(self):
        """
        The WSGI application attribute name, as a string.

        In the example above, application_attrubute_name should be "application".
        """
        raise NotImplementedError

    @property
    def middleware_name(self):
        """
        The name of the middleware containing the RequestContext instance that is
        used for requests to the application being tested. One day this will be
        unnecessary, as it will only be WSGIMiddleware.
        """
        raise NotImplementedError

    @property
    def middleware_request_context(self):
        return "contrast.agent.middlewares.{}.RequestContext".format(
            self.middleware_name
        )

    def setup_method(self):
        self.create_mocks()
        self.build_app()

    def teardown_method(self):
        self.settings_patch.stop()
        self.request_context_patch.stop()
        clear_properties()

        # this forces each new test to use a newly initialized application (& middleware)
        del sys.modules[self.application_module_name]

    def create_mocks(self):
        self.settings = self.build_settings()
        mock_settings = mock.MagicMock(return_value=self.settings)
        self.settings_patch = mock.patch(SETTINGS_STATE_PATCH_LOC, mock_settings)

        self.request_context_patch = mock.patch(
            self.middleware_request_context, self.patch_request_context()
        )

        self.settings_patch.start()
        self.request_context_patch.start()

    def build_settings(self):
        """Override in subclasses to use different settings."""
        return SettingsBuilder().build()

    def patch_request_context(self):
        class PatchedRequestContext(RequestContext):
            def __init__(*args, **kwargs):
                super(PatchedRequestContext, args[0]).__init__(*args[1:], **kwargs)
                # This "self" belongs to the test class, not the request context
                self.request_context = args[0]

        return PatchedRequestContext

    def build_app(self):
        """
        Override to configure the app for each middleware. The goal of this configuration
        is to rebuild the WSGI application (and reinitialize the Contrast middleware) for
        each test. This way we avoid state bleeding across tests.
        """
        app_module = importlib.import_module(self.application_module_name)
        self.app = getattr(app_module, self.application_attribute_name)
        self.client = TestApp(self.app, lint=False)

    @classmethod
    def teardown_class(cls):
        """
        Patch locations that are used by both assess and protect tests need to be
        reversed here.
        """
        patch_manager.reverse_patches_by_owner(os)
        patch_manager.reverse_patches_by_owner(subprocess)
        patch_manager.reverse_patches_by_owner(subprocess.Popen)
        patch_manager.reverse_patches_by_owner(pickle)

        pymongo_module = sys.modules.get("pymongo.collection")
        if pymongo_module:
            patch_manager.reverse_patches_by_owner(pymongo_module.Collection)
