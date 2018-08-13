import os
from flask import Flask, render_template, request, redirect, url_for, make_response

from mastodon import Mastodon, get_client_keys, generate_oauth_url, process_refresh_token
from tootsaver_data import save_toot, read_saved, remove_data, call_data

root_dir = os.path.abspath(os.path.dirname(__file__))

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
    user_id = request.cookies.get("account_id", None)
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
    refresh_token = request.args.get("code", default=None, type=str)
    host_domain = request.cookies.get("host_domain", "")
    client_keys = get_client_keys(root_dir, host_domain)
    if not refresh_token == None:
        access_token = process_refresh_token(
            host_domain, client_keys[0], client_keys[1], refresh_token)
        response = make_response(redirect(url_for("regulusaurum_dashboard")))
        api = Mastodon(access_token=access_token, host_domain=host_domain)
        result = api.verify_credentials().json()
        account_id = result["id"]
        response.set_cookie("account_id", value=account_id)
        screen_name = result["username"]
        response.set_cookie("screen_name", screen_name)
        return response
    else:
        return redirect(url_for("regulusaurum_info", requireLogin=0))


@app.route("/regulusaurum/dashboard", methods=["GET"])
def regulusaurum_dashboard():
    account_id = request.cookies.get("account_id", None)
    if account_id == None:
        return redirect(url_for("regulusaurum_info", requireLogin=0))
    else:
        title = "ユーザーページ - EasyTootSaver ~獅子の黄金~"
        return render_template("regulusaurum/dashboard.html", title=title)


@app.route("/tuskyex", methods=["GET"])
def tuskyex():
    title = "TuskyEx Kyori Build"
    tuskyex_root=root_dir+"/tuskyex"
    version_name_list=os.listdir(tuskyex_root)
    version_name_list.sort()
    version_name_list.reverse()
    view_array=[]
    for file_name in version_name_list:
        file_path=tuskyex_root+"/"+file_name
        with open(file_path,"r",encoding="utf-8") as input:
            text=input.read()
        joker={}
        joker["version"]=file_name
        joker["apk_url"]=url_for("static",filename="apk/"+file_name+".apk")
        joker["content"]=text
        view_array.append(joker)
    return render_template("tuskyex.html", title=title, view_array=view_array)


@app.route("/profile", methods=["GET"])
def profile():
    title = "About きょり/わんせた"
    return render_template("profile.html", title=title)


if __name__ == "__main__":
    app.run(host="localhost", port=1443)
