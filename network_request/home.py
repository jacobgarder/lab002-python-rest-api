from flask import render_template, request, Blueprint, session
from flask import g
import logging
from network_request.auth import tacacs_accounting_access
from network_request.services import service_list
from .models.VLAN_Service import VLAN_Service
from .models.TACACS_Auth import TACACS_Auth
from uuid import uuid4

bp = Blueprint("home", __name__)


@bp.route("/", methods=["GET", "POST"])
@bp.route("/home", methods=["GET", "POST"])
@tacacs_accounting_access
def home():
    if request.method == "POST" and session.get("authenticated"):
        logging.info(
            f"New Service Request from [{request.form['submitter']}] for VLAN Name [{request.form['name']}]"
        )
        # Add new service entry
        tacacs = TACACS_Auth()
        tacacs.accounting(
            username=g.username,
            action="submit-request",
            message=f"New Service Request from [{request.form['submitter']}] for VLAN Name [{request.form['name']}] Description [{request.form['description']}]",
        )
        service_list[uuid4().int] = VLAN_Service(
            name=request.form["name"],
            description=request.form["description"],
            submitter=request.form["submitter"],
        )

    return render_template("home.j2", service_list=service_list)
