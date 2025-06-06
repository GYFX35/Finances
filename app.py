from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import datetime

app = Flask(__name__)

user_profiles_db = {
    1: {
        "username": "testuser",
        "display_name": "Test User",
        "bio": "This is a test bio."
    }
}
next_user_id = 2

business_profiles_db = {
    1: {
        "name": "Test Business Inc.",
        "description": "A sample business for testing purposes.",
        "industry": "Software Development",
        "location": "Anytown, USA",
        "contact_email": "contact@testbusiness.com",
        "website_url": "http://testbusiness.com",
        "submitted_by_user_id": 1, # Assuming user 1 submitted it
        "comments": [ # Add an empty list for comments as per plan step 4
            {"author_name": "JaneD", "text": "Great initiative!"}
        ]
    }
}
next_business_id = 2 # Since we added business 1

marketing_forum_threads_db = {
    1: {
        "title": "Welcome to the Marketing Forum!",
        "initial_post_content": "This is the first thread. Let's discuss amazing marketing strategies!",
        "author_name": "AdminUser", # Could be linked to a user_id if users are submitting threads
        "created_at": datetime.datetime.now(),
        "replies": [
            {
                "reply_author_name": "Commenter1",
                "reply_content": "Great to be here! Looking forward to discussions.",
                "replied_at": datetime.datetime.now() - datetime.timedelta(minutes=30) # Sample time
            }
        ]
    }
}
next_marketing_thread_id = 2 # Since we added thread 1

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

@app.route('/businesses/create', methods=['GET', 'POST'])
def create_business():
    global next_business_id
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        industry = request.form.get('industry', '') # .get for optional fields
        location = request.form.get('location', '')
        contact_email = request.form.get('contact_email', '')
        website_url = request.form.get('website_url', '')

        current_id = next_business_id
        next_business_id += 1

        new_business = {
            "business_id": current_id, # Explicitly adding business_id to the dict
            "name": name,
            "description": description,
            "industry": industry,
            "location": location,
            "contact_email": contact_email,
            "website_url": website_url,
            "submitted_by_user_id": 1,  # Placeholder user ID
            "comments": []  # Initialize with an empty list for comments
        }
        business_profiles_db[current_id] = new_business

        # Assuming 'view_business_profile' will be the function name for the profile page
        return redirect(url_for('view_business_profile', business_id=current_id))
    return render_template('create_business.html')

@app.route('/business/<int:business_id>')
def view_business_profile(business_id):
    business = business_profiles_db.get(business_id)
    if business:
        return render_template('business_profile.html', business=business)
    else:
        abort(404)

@app.route('/business/<int:business_id>/add_comment', methods=['POST'])
def add_comment_to_business(business_id):
    business = business_profiles_db.get(business_id)
    if not business:
        abort(404)

    author_name = request.form.get('author_name')
    comment_text = request.form.get('comment_text')

    if not author_name or not comment_text:
        # Or handle more gracefully, e.g., flash a message and redirect
        abort(400) # Bad request if required fields are missing

    business['comments'].append({
        "author_name": author_name,
        "text": comment_text
    })

    return redirect(url_for('view_business_profile', business_id=business_id))

# Marketing Forum Routes
@app.route('/marketing-forum')
def view_marketing_forum():
    # Sorting will be handled in the template for simplicity here
    return render_template('marketing_forum.html', threads=marketing_forum_threads_db)

@app.route('/marketing-forum/new', methods=['GET', 'POST'])
def create_marketing_thread():
    global next_marketing_thread_id
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        title = request.form.get('title')
        initial_post_content = request.form.get('initial_post_content')

        if not author_name or not title or not initial_post_content:
            # Handle error: all fields are required
            # For simplicity, aborting, but a redirect with flash message would be better
            abort(400, description="Author name, title, and content are required.")

        current_thread_id = next_marketing_thread_id

        new_thread = {
            "title": title,
            "initial_post_content": initial_post_content,
            "author_name": author_name,
            "created_at": datetime.datetime.now(),
            "replies": []
        }
        marketing_forum_threads_db[current_thread_id] = new_thread
        next_marketing_thread_id += 1

        # Assuming 'view_marketing_thread_and_replies' will be the function name for the thread detail page
        return redirect(url_for('view_marketing_thread_and_replies', thread_id=current_thread_id))

    return render_template('create_marketing_thread.html')

@app.route('/marketing-forum/thread/<int:thread_id>')
def view_marketing_thread_and_replies(thread_id):
    thread_data = marketing_forum_threads_db.get(thread_id)
    if not thread_data:
        abort(404)
    return render_template('view_marketing_thread.html', thread=thread_data, thread_id=thread_id)

@app.route('/marketing-forum/thread/<int:thread_id>/add_reply', methods=['POST'])
def add_marketing_reply(thread_id):
    thread_data = marketing_forum_threads_db.get(thread_id)
    if not thread_data:
        abort(404)

    reply_author_name = request.form.get('reply_author_name')
    reply_content = request.form.get('reply_content')

    if not reply_author_name or not reply_content:
        # For simplicity, aborting, but a redirect with flash message would be better
        abort(400, description="Author name and reply content are required.")

    new_reply = {
        "reply_author_name": reply_author_name,
        "reply_content": reply_content,
        "replied_at": datetime.datetime.now()
    }

    marketing_forum_threads_db[thread_id]['replies'].append(new_reply)

    return redirect(url_for('view_marketing_thread_and_replies', thread_id=thread_id))

@app.route('/offline')
def offline_page():
    return render_template('offline.html')

@app.route('/sw.js')
def service_worker_route(): # Renamed function to avoid conflict if 'service_worker' is used elsewhere
    return send_from_directory(app.root_path, 'sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=True)
