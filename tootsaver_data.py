import os
import json

# serverディレクトリ構造
# server/
#     keys.json アクセストークンの保管場所
#     0.json    ユーザー0の保存ファイル
#     57.json   ユーザー57の保存ファイル
#
# keys.json     "獅子の黄金 アカウント確認"のトークンの保存場所
# {"token" : "access_token", "インスタンスのホスト名" : ["client_key", "client_secret"]}
#
# userid.json   ユーザーごとの保存場所
# [["tag", "url"]]


# account_id : アプリ実行側インスタンスから見た一意のint id
def save_toot(root_dir, account_id, tag, save_url, api, request_toot, reply_to):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    file_path = root_dir+"/"+account_id+".json"
    saved_array = read_saved(root_dir, account_id)
    action_flag = True
    for item in saved_array:
        if action_flag:
            if item[0] == tag:
                if item[1] == save_url:
                    saved_array.remove(item)
                    api.toot("Removed : "+save_url+" -> " +
                             tag, request_toot, reply_to)
                    action_flag = False
    if action_flag:
        saved_array.append([tag, save_url])
        api.toot("Registered : "+save_url+" -> "+tag, request_toot, reply_to)
    with open(file_path, "w") as output:
        output.write(json.dumps(saved_array))


def read_saved(root_dir, account_id):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    file_path = root_dir+"/"+account_id+".json"
    if os.path.exists(file_path):
        with open(file_path, "r") as input:
            text = input.read()
        return json.loads(text)
    else:
        return []


def remove_data(root_dir, account_id):
    file_path = root_dir+"/"+account_id+".json"
    os.remove(file_path)


def call_data(root_dir, account_id, tag, api, request_toot, reply_to):
    text = "Calling saved toots with tag : "+tag+"\n"
    saved_array = read_saved(root_dir, account_id)
    for item in saved_array:
        if item[0] == tag:
            text = text+item[1]+"\n"
    api.toot(text, request_toot, reply_to)
