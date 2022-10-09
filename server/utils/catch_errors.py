import traceback
from functools import wraps

from utils.exceptions import HandledException


def catch_errors(endpoint):
    @wraps(endpoint)
    def wrap(*args, **kwargs):
        try:
            return endpoint(*args, **kwargs)
        
        except HandledException as e:
            return e.message, e.status_code
        
        except Exception as e:
            return traceback.format_exc(), 500

    return wrap
