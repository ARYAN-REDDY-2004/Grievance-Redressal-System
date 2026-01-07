from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from data import complaints,ENGINEERS,USERS

app = Flask(__name__)

# Home pages
# Home pages
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/citizen")
def citizen():
    return render_template("citizen.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


# Register complaint
@app.route("/complaint", methods=["POST"])
def register_complaint():
    data = request.json
    engineer = ENGINEERS[data["type"]]
    sla_days = 2 if data["type"] == "Water" else 7
    deadline = datetime.now() + timedelta(days=sla_days)

    complaint = {
        "id": len(complaints) + 1,
        "issue": data["issue"],
        "description": data["description"], 
        "type": data["type"],
        "engineer_id": engineer["id"],
        "officer": engineer["name"],
        "deadline": deadline.strftime("%Y-%m-%d"),
        "status": "Assigned"
    }

    complaints.append(complaint)
    return jsonify({"message": "Complaint Registered", "complaint": complaint})

# Update complaint status
@app.route("/update/<int:cid>", methods=["POST"])
def update_status(cid):
    for c in complaints:
        if c["id"] == cid:
            c["status"] = request.json["status"]
            return jsonify({"message": "Status Updated"})
    return jsonify({"error": "Not found"})

# Get all complaints (Admin view)
@app.route("/complaints")
def get_complaints():
    now = datetime.now()

    for c in complaints:
        deadline = datetime.strptime(c["deadline"], "%Y-%m-%d")

        if now > deadline and c["status"] != "Resolved":
            c["status"] = "Escalated"
            c["officer"] = "Executive Engineer"

    return jsonify(complaints)

@app.route("/login", methods=["POST"])
def login_post():
    data = request.json
    email = data.get("username")
    password = data.get("password")
    role = data.get("role")

    for user in USERS:
        if user["email"] == email and user["password"] == password and user["role"] == role:
            redirect_url = "/citizen" if role == "citizen" else "/admin"
            return jsonify({"success": True, "redirect": redirect_url})

    return jsonify({"success": False})



if __name__ == "__main__":
    app.run(debug=True)

