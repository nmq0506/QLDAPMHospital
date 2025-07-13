import data,json
def auth_user(username, password):
    with open("data/data.json", encoding="utf-8") as f:
        users= json.load(f)
        for u in users:
            if u["username"]==username and u["password"]== password:
                return True
    return False