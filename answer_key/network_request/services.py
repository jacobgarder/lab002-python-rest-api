from flask import render_template, request, Blueprint
from flask import g
from .auth import read_right_required, tacacs_accounting_access
from .models.TACACS_Auth import TACACS_Auth
import logging

bp = Blueprint("services", __name__)

service_list = {}


@bp.route("/services", methods=["GET", "POST"])
@read_right_required
@tacacs_accounting_access
def services():
    if request.method == "POST":
        action = request.form["action"]
        uuid = int(request.form["uuid"])
        vid = request.form["vid"]
        logging.info(
            f"User [{g.username}] taking Service management Action [{action}] for UUID [{uuid}] VLAN ID [{vid}]"
        )
        tacacs = TACACS_Auth()
        tacacs.accounting(
            username=g.username,
            action="request-management",
            message=f"User [{g.username}] taking Service management Action [{action}] for UUID [{uuid}] VLAN ID [{vid}]",
        )
        service_list[uuid].id = vid
        service_list[uuid].status = action
    return render_template("services.j2", service_list=service_list)
