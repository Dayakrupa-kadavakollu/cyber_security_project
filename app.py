from flask import Flask, render_template, request

app = Flask(__name__)

request_count = {}
blocked_ips = []
logs = []

# AI Defense
def get_defense(attack):
    if attack == "Phishing":
        return "Email Filtering + Awareness"
    elif attack == "Malware":
        return "Antivirus + Sandbox"
    elif attack == "DDoS":
        return "Firewall + Rate Limiting"
    elif attack == "Password Attack":
        return "MFA + Strong Password"
    else:
        return "No Defense"

# Detect attack
def detect_attack(ip):
    if ip in request_count:
        request_count[ip] += 1
    else:
        request_count[ip] = 1

    if request_count[ip] > 5:
        return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                           total_users=len(request_count),
                           blocked=len(blocked_ips))

@app.route('/simulate', methods=['POST'])
def simulate():
    ip = request.remote_addr

    if ip in blocked_ips:
        return "ACCESS DENIED 🚫 (You are blocked)"

    attack = request.form['attack']
    is_attack = detect_attack(ip)
    defense = get_defense(attack)

    if is_attack:
        blocked_ips.append(ip)
        status = "USER BLOCKED 🚫"
    else:
        status = "ATTACK BLOCKED ✅"

    # ✅ LOG SAVE (important)
    logs.append({
        "ip": ip,
        "attack": attack,
        "defense": defense,
        "status": status
    })

    return render_template('result.html',
                           attack=attack,
                           defense=defense,
                           status=status,
                           ip=ip)

# ✅ LOGS PAGE ROUTE (important)
@app.route('/logs')
def show_logs():
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
