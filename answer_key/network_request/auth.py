import functools

from flask import render_template, request, Blueprint, session, redirect, url_for
from flask import g
from .models.TACACS_Auth import TACACS_Auth

bp = Blueprint("auth", __name__)


def login_required(view):
    """Decorator to require logged in user, or redirect to login."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def read_right_required(view):
    """Decorator to require user with read rights."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("rights")["read"]:
            return redirect(url_for("home.home"))

        return view(**kwargs)

    return wrapped_view


def tacacs_accounting_access(view):
    """Decorator to make TACACS accounting when page viewed."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        username = g.username if g.username else "None"
        tacacs = TACACS_Auth()
        tacacs.accounting(
            username=username,
            action="page-access",
            message=f"Application page [{request.path}] accessed by [{g.username}] from remote_addr [{request.remote_addr}]",
        )

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def get_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    g.username = session.get("username")
    g.authenticated = session.get("authenticated")
    g.rights = session.get("rights")


@bp.route("/login", methods=["GET", "POST"])
@tacacs_accounting_access
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session.clear()
        tacacs = TACACS_Auth()
        tacacs.accounting(
            username=username,
            action="login",
            message=f"username '{username}' attempting to login",
        )
        authenticate = tacacs.authenticate(username, password)
        if authenticate:
            tacacs.accounting(
                username=username,
                action="login",
                message=f"username '{username}' logged in",
            )
            session["username"] = username
            session["authenticated"] = True
            tacacs.accounting(
                username=username,
                action="authorize",
                message=f"username '{username}' attempting to authorize",
            )
            rights = tacacs.authorize(username)
            session["rights"] = rights
        # TODO: Add error if authentication failed
        return redirect(url_for("home.home"))
    else:
        return render_template("login.j2")


@bp.route("/logout")
@tacacs_accounting_access
def logout():
    """Logout from application"""
    username = session.get("username")
    if username:
        tacacs = TACACS_Auth()
        tacacs.accounting(
            username=username,
            action="logout",
            message=f"username '{username}' logging out",
        )
    session.clear()
    return redirect(url_for("home.home"))


@bp.route("/user/profile")
@login_required
@tacacs_accounting_access
def profile():
    """Show the profile for a logged in user."""
    username = session.get("username")
    rights = session["rights"]

    tacacs = TACACS_Auth()
    tacacs.accounting(
        username=username,
        action="view",
        message=f"username '{username}' is viewing their profile",
    )

    return render_template("profile.j2", username=username, rights=rights)
