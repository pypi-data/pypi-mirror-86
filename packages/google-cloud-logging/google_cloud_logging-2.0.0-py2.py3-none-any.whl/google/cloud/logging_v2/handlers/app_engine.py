# Copyright 2016 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logging handler for App Engine Flexible

Sends logs to the Cloud Logging API with the appropriate resource
and labels for App Engine logs.
"""

import logging
import os

from google.cloud.logging_v2.handlers._helpers import get_trace_id
from google.cloud.logging_v2.handlers.transports import BackgroundThreadTransport
from google.cloud.logging_v2.resource import Resource

_DEFAULT_GAE_LOGGER_NAME = "app"

_GAE_PROJECT_ENV_FLEX = "GCLOUD_PROJECT"
_GAE_PROJECT_ENV_STANDARD = "GOOGLE_CLOUD_PROJECT"
_GAE_SERVICE_ENV = "GAE_SERVICE"
_GAE_VERSION_ENV = "GAE_VERSION"

_TRACE_ID_LABEL = "appengine.googleapis.com/trace_id"


class AppEngineHandler(logging.StreamHandler):
    """A logging handler that sends App Engine-formatted logs to Stackdriver."""

    def __init__(
        self,
        client,
        *,
        name=_DEFAULT_GAE_LOGGER_NAME,
        transport=BackgroundThreadTransport,
        stream=None,
    ):
        """
        Args:
            client (~logging_v2.client.Client): The authenticated
                Google Cloud Logging client for this handler to use.
            name (Optional[str]): Name for the logger.
            transport (Optional[~logging_v2.transports.Transport]):
                The transport class. It should be a subclass
                of :class:`.Transport`. If unspecified,
                :class:`.BackgroundThreadTransport` will be used.
            stream (Optional[IO]): Stream to be used by the handler.

        """
        super(AppEngineHandler, self).__init__(stream)
        self.name = name
        self.client = client
        self.transport = transport(client, name)
        self.project_id = os.environ.get(
            _GAE_PROJECT_ENV_FLEX, os.environ.get(_GAE_PROJECT_ENV_STANDARD, "")
        )
        self.module_id = os.environ.get(_GAE_SERVICE_ENV, "")
        self.version_id = os.environ.get(_GAE_VERSION_ENV, "")
        self.resource = self.get_gae_resource()

    def get_gae_resource(self):
        """Return the GAE resource using the environment variables.

        Returns:
            google.cloud.logging_v2.resource.Resource: Monitored resource for GAE.
        """
        gae_resource = Resource(
            type="gae_app",
            labels={
                "project_id": self.project_id,
                "module_id": self.module_id,
                "version_id": self.version_id,
            },
        )
        return gae_resource

    def get_gae_labels(self):
        """Return the labels for GAE app.

        If the trace ID can be detected, it will be included as a label.
        Currently, no other labels are included.

        Returns:
            dict: Labels for GAE app.
        """
        gae_labels = {}

        trace_id = get_trace_id()
        if trace_id is not None:
            gae_labels[_TRACE_ID_LABEL] = trace_id

        return gae_labels

    def emit(self, record):
        """Actually log the specified logging record.

        Overrides the default emit behavior of ``StreamHandler``.

        See https://docs.python.org/2/library/logging.html#handler-objects

        Args:
            record (logging.LogRecord): The record to be logged.
        """
        message = super(AppEngineHandler, self).format(record)
        gae_labels = self.get_gae_labels()
        trace_id = (
            "projects/%s/traces/%s" % (self.project_id, gae_labels[_TRACE_ID_LABEL])
            if _TRACE_ID_LABEL in gae_labels
            else None
        )
        self.transport.send(
            record, message, resource=self.resource, labels=gae_labels, trace=trace_id
        )
