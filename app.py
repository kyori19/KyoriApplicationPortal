from flask import Flask, render_template, request, redirect, url_for, make_response

from mastodon import Mastodon, get_client_keys, generate_oauth_url
from tootsaver_data import save_toot, read_saved, remove_data, call_data

root_dir = "/home/portal/app/server"

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    title = "Kyori Application Portal"
    return render_template("index.html", title=title)


@app.route("/regulusaurum", methods=["GET"])
def regulusaurum():
    return redirect(url_for("regulusaurum_info"))


@app.route("/regulusaurum/info", methods=["GET"])
def regulusaurum_info():
    user_id = request.cookies.get("user_id", None)
    if user_id == None:
        title = "ログイン・利用登録 - EasyTootSaver ~獅子の黄金~"
        requireLogin = request.args.get("requireLogin", default=1, type=int)
        return render_template("regulusaurum/info.html", title=title, requireLogin=requireLogin)
    else:
        return redirect(url_for("regulusaurum_dashboard"))


@app.route("/regulusaurum/jump", methods=["POST"])
def regulusaurum_jump():
    host_domain = request.form.get("host_domain")
    client_keys = get_client_keys(root_dir, host_domain)
    response = make_response(redirect(generate_oauth_url(
        host_domain, client_keys[0], "https://app.odakyu.app/regulusaurum/done", "read:accounts")))
    response.set_cookie("host_domain", value=host_domain)
    return response


@app.route("/regulusaurum/done", methods=["GET"])
def regulusaurum_done():
    access_token = request.args.get("code", default=None, type=str)
    host_domain = request.cookies.get("host_domain", "")
    if not access_token == None:
        response = make_response(redirect(url_for("regulusaurum_dashboard")))
        response.set_cookie("access_token", value=access_token)
        api = Mastodon(access_token, host_domain)
        result = api.verify_credentials()
        account_id = result["id"]
        response.set_cookie("account_id", value=account_id)
        screen_name = result["screen_name"]
        response.set_cookie("screen_name", screen_name)
        return response
    else:
        return redirect(url_for("regulusaurum_info", requireLogin=0))


@app.route("/regulusaurum/dashboard", methods=["GET"])
def regulusaurum_dashboard():
    user_id = request.cookies.get("user_id", None)
    if user_id == None:
        return redirect(url_for("regulusaurum_info", requireLogin=0))
    else:
        title = "ユーザーページ - EasyTootSaver ~獅子の黄金~"
        return render_template("regulusaurum/dashboard.html", title=title)


@app.route("/profile", methods=["GET"])
def profile():
    title = "About きょり/わんせた"
    return render_template("profile.html", title=title)


if __name__ == "__main__":
    app.run(host="localhost", port=1443)
