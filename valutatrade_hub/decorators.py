import functools
import inspect
import sys

from valutatrade_hub.logging_config import logger


def log_action(func):
    """Декоратор для логирования действий (buy, sell)."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        action_name = func.__name__.upper()
        
        usecases_module = sys.modules.get("valutatrade_hub.core.usecases")
        username = "unknown"
        if usecases_module and hasattr(usecases_module, "current_user"):
            user = usecases_module.current_user
            if user:
                username = user.get("username", "unknown")
        
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        args_parts = []
        for name, value in bound_args.arguments.items():
            args_parts.append(f"{name}={value!r}")
        args_str = " ".join(args_parts)
        
        try:
            result = func(*args, **kwargs)
            
            logger.info(
                f"ACTION={action_name} user='{username}' {args_str} result=OK"
            )
            return result
            
        except Exception as e:
            logger.error(
                f"ACTION={action_name} user='{username}' {args_str} result=ERROR error='{e}'"
            )
            raise
            
    return wrapper