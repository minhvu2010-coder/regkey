from flask import Flask, request, jsonify
import time

app = Flask(__name__)

keys_db = {}  # lưu RAM, thích thì lưu file JSON


# ================= CREATE KEY =================
@app.route("/create")
def create_key():
    ip = request.args.get("ip")
    day = int(request.args.get("day", 1))
    password = request.args.get("pass")

    if password != "admin123":
        return jsonify({"status": False, "msg": "Sai mật khẩu admin"})

    expire = time.time() + day * 86400

    key = f"KEY-{int(time.time())}"
    keys_db[key] = {
        "ip": ip,
        "expire": expire
    }

    return jsonify({
        "status": True,
        "key": key,
        "expire": expire
    })


# ================= CHECK KEY =================
@app.route("/check")
def check():
    key = request.args.get("key")
    ip = request.args.get("ip")

    if key not in keys_db:
        return jsonify({"status": False, "msg": "Key không tồn tại"})

    data = keys_db[key]

    if data["ip"] != ip:
        return jsonify({"status": False, "msg": "Sai IP"})

    if time.time() > data["expire"]:
        return jsonify({"status": False, "msg": "Key hết hạn"})

    return jsonify({"status": True, "msg": "OK"})


app.run(host="0.0.0.0", port=5000)