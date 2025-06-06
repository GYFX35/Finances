from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

user_profiles_db = {
    1: {
        "username": "testuser",
        "display_name": "Test User",
        "bio": "This is a test bio."
    }
}
next_user_id = 2

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global next_user_id
    if request.method == 'POST':
        username = request.form['username']
        display_name = request.form['display_name']
        bio = request.form['bio']

        current_id = next_user_id
        next_user_id += 1

        user_profiles_db[current_id] = {
            "username": username,
            "display_name": display_name,
            "bio": bio
        }
        return redirect(url_for('view_profile', user_id=current_id))
    return render_template('signup.html')

@app.route('/profile/<int:user_id>')
def view_profile(user_id):
    user = user_profiles_db.get(user_id)
    if user:
        return render_template('profile.html', user=user)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
