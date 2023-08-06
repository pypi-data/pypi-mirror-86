import structlog

from . import signals


logger = structlog.getLogger(__name__)


def receiver_before_task_publish(sender=None, headers=None, body=None, **kwargs):
    immutable_logger = structlog.threadlocal.as_immutable(logger)
    # noinspection PyProtectedMember
    context = dict(immutable_logger._context)
    if "task_id" in context:
        context["parent_task_id"] = context.pop("task_id")

    signals.modify_context_before_task_publish.send(
        sender=receiver_before_task_publish, context=context
    )

    import celery

    if celery.VERSION > (4,):
        headers["__django_structlog__"] = context
    else:
        body["__django_structlog__"] = context


def receiver_after_task_publish(sender=None, headers=None, body=None, **kwargs):
    logger.info(
        "task_enqueued",
        child_task_id=headers.get("id") if headers else body.get("id"),
        child_task_name=headers.get("task") if headers else body.get("task"),
    )


def receiver_task_pre_run(task_id, task, *args, **kwargs):
    logger.new()
    logger.bind(task_id=task_id)
    metadata = getattr(task.request, "__django_structlog__", {})
    logger.bind(**metadata)
    signals.bind_extra_task_metadata.send(
        sender=receiver_task_pre_run, task=task, logger=logger
    )


def receiver_task_retry(request=None, reason=None, einfo=None, **kwargs):
    logger.warning("task_retrying", reason=reason)


def receiver_task_success(result=None, **kwargs):
    with structlog.threadlocal.tmp_bind(logger):
        signals.pre_task_succeeded.send(
            sender=receiver_task_success, logger=logger, result=result
        )
        logger.info("task_succeeded")


def receiver_task_failure(
    task_id=None, exception=None, traceback=None, einfo=None, *args, **kwargs
):
    logger.exception("task_failed", error=str(exception), exception=exception)


def receiver_task_revoked(
    request=None, terminated=None, signum=None, expired=None, **kwargs
):
    logger.warning(
        "task_revoked", terminated=terminated, signum=signum, expired=expired
    )


def receiver_task_unknown(message=None, exc=None, name=None, id=None, **kwargs):
    logger.error("task_not_found", message=message)


def receiver_task_rejected(message=None, exc=None, **kwargs):
    logger.error("task_rejected", message=message)
