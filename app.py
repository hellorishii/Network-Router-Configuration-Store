
from flask import Flask, render_template, request, redirect, url_for, flash

from router_store import add_router, get_routers, delete_router

app = Flask(__name__)

app.secret_key = "router-project-secret-key"


@app.route("/")
def home():

    routers = get_routers()

    search = request.args.get("search", "").strip()

    if search:
        routers = {
            name: config
            for name, config in routers.items()
            if search.lower() in name.lower()
        }

    return render_template(
        "index.html",
        routers=routers,
        search=search
    )


@app.route("/add", methods=["POST"])
def add():

    device_name = request.form.get("device_name", "")
    ip_address = request.form.get("ip_address", "")
    port = request.form.get("port", "")

    success, message = add_router(
        device_name,
        ip_address,
        port
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("home"))


@app.route("/delete/<device_name>", methods=["POST"])
def delete_router_route(device_name):

    success, message = delete_router(device_name)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
