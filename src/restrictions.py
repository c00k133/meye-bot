from functools import wraps
import json

# secrets = json.load(open("../token.json"))
# LIST_OF_ADMINS = list(map(lambda s: s["id"], secrets["auth_check"]))
LIST_OF_ADMINS = []

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unathorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

