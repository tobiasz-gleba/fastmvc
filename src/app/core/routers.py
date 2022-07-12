from projects.users.view import app as users
from utils.observability import app as healtcheck

routers = (
    (healtcheck, "healtcheck", ["healtcheck"]),
    (users, "auth", ["auth"]),
)
