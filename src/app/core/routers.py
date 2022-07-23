from projects.auth.view import app as auth
from utils.observability import app as healtcheck

routers = (
    (healtcheck, "healtcheck", ["healtcheck"]),
    (auth, "auth", ["auth"]),
)
