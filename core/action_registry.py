from utils.logger import get_logger

logger = get_logger()

class ActionRegistry:
    _actions = {}
    
    @classmethod
    def register(cls, name, category="general"):
        def decorator(func):
            cls._actions[name] = {
                'function': func,
                'category': category,
                'name': name
            }
            logger.debug(f"注册Action Word: {name} (类别: {category})")
            return func
        return decorator
    
    @classmethod
    def get_action(cls, name):
        return cls._actions.get(name)
    
    @classmethod
    def list_actions(cls, category=None):
        if category:
            return {k: v for k, v in cls._actions.items() if v['category'] == category}
        return cls._actions
