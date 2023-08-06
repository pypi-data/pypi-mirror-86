"""Default GitHub event dispatcher."""

from functools import wraps

from .routers import ConcurrentRouter


__all__ = (
    'dispatch_event',
    'process_event',
    'process_event_actions',
    'WEBHOOK_EVENTS_ROUTER',
)


WEBHOOK_EVENTS_ROUTER = ConcurrentRouter()
"""An event dispatcher for webhooks."""


dispatch_event = WEBHOOK_EVENTS_ROUTER.dispatch  # pylint: disable=invalid-name
process_event = WEBHOOK_EVENTS_ROUTER.register  # pylint: disable=invalid-name


def process_event_actions(event_name, actions=None):
    """Subscribe to multiple events."""
    if actions is None:
        actions = []

    def decorator(original_function):

        def wrapper(*args, **kwargs):
            return original_function(*args, **kwargs)

        if not actions:
            wrapper = process_event(event_name)(wrapper)

        for action in actions:
            wrapper = process_event(event_name, action=action)(wrapper)

        return wraps(original_function)(wrapper)

    return decorator
