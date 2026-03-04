from flask import Flask, render_template, request, redirect, url_for, flash  # pyre-ignore
import os
import json
import subprocess

app = Flask(__name__)
app.secret_key = "clara_pipeline_secret" # Needed for flash messages

OUTPUT_DIR = "outputs/accounts"

def load_accounts():
    accounts = []
    
    if not os.path.exists(OUTPUT_DIR):
        return accounts

    for acc in sorted(os.listdir(OUTPUT_DIR)):
        acc_path = os.path.join(OUTPUT_DIR, acc)
        if not os.path.isdir(acc_path):
            continue

        v1_file = os.path.join(acc_path, "v1", "memo.json")
        v2_file = os.path.join(acc_path, "v2", "memo.json")

        v1_data = {}
        v2_data = {}

        if os.path.exists(v1_file):
            with open(v1_file) as f:
                v1_data = json.load(f)

        if os.path.exists(v2_file):
            with open(v2_file) as f:
                v2_data = json.load(f)

        accounts.append({
            "account": acc,
            "v1": json.dumps(v1_data, indent=4) if v1_data else "No v1 data generated yet.",
            "v2": json.dumps(v2_data, indent=4) if v2_data else "No v2 data generated yet."
        })

    return accounts

@app.route("/")
def dashboard():
    accounts = load_accounts()
    return render_template("dashboard.html", accounts=accounts)

@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    try:
        # Run the main.py script
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True, check=True)
        flash("Pipeline executed successfully! Artifacts have been regenerated.", "success")
    except subprocess.CalledProcessError as e:
        flash(f"Error executing pipeline: {e.stderr}", "error")
        
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
