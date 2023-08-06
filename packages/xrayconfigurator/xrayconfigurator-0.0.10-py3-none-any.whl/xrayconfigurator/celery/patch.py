import wrapt
import botocore.client

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.utils import stacktrace
from aws_xray_sdk.ext.boto_utils import inject_header, aws_meta_processor
from aws_xray_sdk.ext.util import construct_xray_header, inject_trace_header
from celery import signals

from core.instrumentation.logging import log


def patch():
    @signals.task_prerun.connect
    def task_prerun(task_id, task, *args, **kwargs):
        log.info("task prerun task_id: " + task_id)
        xray_header = construct_xray_header(task.request)
        print(xray_header.root + " " + xray_header.parent)
        segment = xray_recorder.begin_segment(
            name=task.name,
            traceid=xray_header.root,
            parent_id=xray_header.parent,
        )
        segment.save_origin_trace_header(xray_header)
        segment.put_metadata('task_id', task_id, namespace='celery')

    @signals.task_postrun.connect()
    def task_postrun(task_id, *args, **kwargs):
        log.info("task post run task_id: " + task_id)
        xray_recorder.end_segment()

    @signals.before_task_publish.connect
    def before_task_publish(sender, headers, **kwargs):
        log.info("before taskpublish sender: " + sender)
        current_segment = xray_recorder.current_segment()
        subsegment = xray_recorder.begin_subsegment(
            name=sender,
            namespace='remote',
        )

        if subsegment is None:
            # Not in segment
            return
        subsegment.put_metadata('task_id', headers.get("id"), namespace='celery')
        inject_trace_header(headers, subsegment)

    @signals.after_task_publish.connect
    def xray_after_task_publish(**kwargs):
        log.info("after task publish")
        xray_recorder.end_subsegment()

    @signals.task_failure.connect
    def xray_task_failure(einfo, **kwargs):
        log.info("task_failure")
        segment = xray_recorder.current_segment()
        if einfo:
            stack = stacktrace.get_stacktrace(limit=xray_recorder.max_trace_back)
            segment.add_exception(einfo.exception, stack)
