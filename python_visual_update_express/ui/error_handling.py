import traceback

from python_visual_update_express.data.general_settings import DEBUG_MODE
from python_visual_update_express.ui.notifications import error_notification


def process_error(ex: Exception, self=None) -> None:
    # Enable below line for debugging
    if DEBUG_MODE:
        error_notification(''.join(traceback.format_exception(type(ex), ex, ex.__traceback__)), self)
    else:
        error_notification(str(ex), self)
