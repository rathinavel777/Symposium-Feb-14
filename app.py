from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import add_user, get_all_users, get_stats

app = Flask(__name__)

# Event Data (Single Source of Truth)
TECHNICAL_EVENTS = [
    {"id": "paper_ppt", "name": "Paper Presentation", "desc": "Present research on emerging technologies"},
    {"id": "code_debug", "name": "Code Debugging", "desc": "Identify bugs and fix logical errors"},
    {"id": "project_expo", "name": "Project Expo", "desc": "Showcase hardware or software prototypes"},
    {"id": "tech_quiz", "name": "Technical Quiz", "desc": "Test knowledge of core engineering subjects"}
]

NON_TECHNICAL_EVENTS = [
    {"id": "photography", "name": "Photography", "desc": "Capture symposium moments"},
    {"id": "gaming", "name": "Gaming (E-Sports)", "desc": "Competitive virtual gaming"},
    {"id": "treasure_hunt", "name": "Treasure Hunt", "desc": "Solve clues to find the prize"},
    {"id": "debate", "name": "Debate", "desc": "Discuss and debate current global trends"}
]

app.secret_key = 'super_secret_key_change_this_in_production'

@app.route('/')
def index():
    return render_template('index.html', tech_events=TECHNICAL_EVENTS, non_tech_events=NON_TECHNICAL_EVENTS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin123':  # Hardcoded password for demo
            from flask import session
            session['logged_in'] = True
            return redirect(url_for('admin_page'))
        else:
            return render_template('login.html', error="Invalid Password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    from flask import session
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/register')
def register_page():
    return render_template('register.html', tech_events=TECHNICAL_EVENTS, non_tech_events=NON_TECHNICAL_EVENTS)

@app.route('/api/register', methods=['POST'])
def register_api():
    try:
        data = request.json
        # Basic validation
        required_fields = ['full_name', 'college_name', 'dept_year', 'mobile', 'email', 'accommodation']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "message": f"Missing field: {field}"}), 400
        
        # Events processing
        events_list = data.get('events', [])
        if not events_list:
             return jsonify({"success": False, "message": "Please select at least one event."}), 400
        
        user_data = {
            "full_name": data['full_name'],
            "college_name": data['college_name'],
            "dept_year": data['dept_year'],
            "mobile": data['mobile'],
            "email": data['email'],
            "events": ", ".join(events_list),
            "accommodation": data['accommodation']
        }
        
        if add_user(user_data):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Database error"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/success')
def success_page():
    return render_template('success.html')

@app.route('/admin')
def admin_page():
    from flask import session
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    users = get_all_users()
    stats = get_stats()
    return render_template('admin.html', users=users, stats=stats)

@app.route('/api/stats')
def stats_api():
    return jsonify(get_stats())

if __name__ == '__main__':
    # host='0.0.0.0' makes the server accessible to other devices on the same network
    app.run(debug=True, port=5000, host='0.0.0.0')
