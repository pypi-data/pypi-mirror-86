# coding: utf-8

__author__ = "Ondrej Jurcak"

import logging

from aws_xray_sdk import global_sdk_config
from aws_xray_sdk.core import xray_recorder, patch_all, patch
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.ext.flask_sqlalchemy.query import XRayFlaskSqlAlchemy

from core.config import LazySettings
from core.instrumentation.logging import log
from core.instrumentation.xray.xrayconfigurator import celery


class XRayConfigurator:
    def __init__(self, settings, application) -> None:
        if isinstance(settings, LazySettings):
            self._init_xray(settings.XRAY_ENABLED,
                            settings.XRAY_NAME,
                            settings.XRAY_PLUGINS,
                            settings.XRAY_SAMPLING,
                            settings.XRAY_STREAM_SQL,
                            settings.XRAY_DAEMON,
                            settings.XRAY_PATCH_MODULES,
                            settings.XRAY_SQLALCHEMY,
                            settings.XRAY_LOGGING_ENABLED,
                            settings.XRAY_CELERY,
                            application)
        else:
            self._init_xray(settings.get("XRAY", "ENABLED", False),
                            settings.get("XRAY", "SERVICE_NAME"),
                            settings.get("XRAY", "PLUGINS", "'ECSPlugin', 'EC2Plugin'"),
                            settings.get("XRAY", "SAMPLING", False),
                            settings.get("XRAY", "STREAM_SQL", True),
                            settings.get("XRAY", "DAEMON", "xray-daemon:2000"),
                            settings.get("XRAY", "PATCH_MODULES", None),
                            settings.get("XRAY", "SQLALCHEMY", True),
                            settings.get("XRAY", "LOGGING_ENABLED", False),
                            settings.get("XRAY", "CELERY", False),
                            application)

    def _init_xray(self, enabled, name, plugins, sampling, stream_sql, daemon, patch_modules, sqlalchemy, logging_enabled, celery_enabled, application):
        if enabled:
            log.info("xray sdk enabled " + str(enabled))
            global_sdk_config.set_sdk_enabled(True)
            xray_recorder.configure(service=name,
                                    plugins=eval(plugins),
                                    sampling=sampling,
                                    stream_sql=stream_sql,
                                    daemon_address=daemon,
                                    context_missing="LOG_ERROR")
            if not patch_modules:
                patch_all()
            else:
                patch(eval(patch_modules))

            if sqlalchemy:
                log.info("XRayFlaskSqlAlchemy enabled")
                XRayFlaskSqlAlchemy(application)

            XRayMiddleware(application, xray_recorder)

            if logging_enabled:
                log.info("XRay logging enabled")
                logging.getLogger("aws_xray_sdk").setLevel(logging.DEBUG)
            else:
                log.info("XRay logging disabled")
                logging.getLogger("aws_xray_sdk").setLevel(logging.NOTSET)

            if celery_enabled:
                log.info("celery patched")
                celery.patch()
        else:
            log.info("xray sdk disabled")
            global_sdk_config.set_sdk_enabled(False)



