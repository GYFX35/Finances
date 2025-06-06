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

sales_transactions_db = {
    1: {
        "date": datetime.datetime.now() - datetime.timedelta(days=1), # Sample: yesterday
        "product_description": "Super Widget - Model X",
        "quantity": 2,
        "unit_price": 25.00,
        "total_amount": 50.00,
        "customer_info": "Customer Alpha",
        "payment_method": "Credit Card",
        "status": "Completed", # Options: "Completed", "Pending", "Refunded"
        "recorded_by_user_id": 1, # Placeholder
        "comments": [
            {
                "author_name": "SupportTeam",
                "text": "Order processed and shipped.",
                "timestamp": datetime.datetime.now() - datetime.timedelta(hours=23)
            }
        ]
    }
}
next_sales_transaction_id = 2 # Since we added transaction 1

# Banks Data Model
banks_db = {
    1: {
        "name": "Global Trust Bank",
        "description": "A leading international bank providing comprehensive financial services.",
        "website_url": "http://examplebank.com",
        "hq_location": "New York, USA",
        "services": ["Retail Banking", "Wealth Management", "Corporate Loans"],
        "comments": [
            {
                "author_name": "User123",
                "text": "Great customer service!",
                "timestamp": datetime.datetime.now() - datetime.timedelta(days=5)
            }
        ]
    }
}
next_bank_id = 2

# Fintech Tools Data Model
fintech_tools_db = {
    1: {
        "name": "BudgetMaster Pro",
        "description": "An intuitive app for personal and family budget management.",
        "website_url": "http://budgetmasterpro.com",
        "category": "Budgeting",
        "pricing_model": "Freemium", # e.g., Free, Subscription, One-time, Freemium
        "comments": [
            {
                "author_name": "Budgeteer22",
                "text": "Helped me save so much money!",
                "timestamp": datetime.datetime.now() - datetime.timedelta(days=3)
            }
        ]
    }
}
next_fintech_tool_id = 2

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

# Sales Transactions Routes
@app.route('/sales')
def view_sales_list():
    # Sorting is handled in the template
    return render_template('sales_list.html', sales=sales_transactions_db)

@app.route('/sales/new', methods=['GET', 'POST'])
def log_new_sale():
    global next_sales_transaction_id
    if request.method == 'POST':
        product_description = request.form.get('product_description')
        quantity_str = request.form.get('quantity')
        unit_price_str = request.form.get('unit_price')
        customer_info = request.form.get('customer_info', '') # Optional
        payment_method = request.form.get('payment_method', '') # Optional
        status = request.form.get('status', 'Pending') # Default to Pending

        if not product_description or not quantity_str or not unit_price_str:
            abort(400, description="Product description, quantity, and unit price are required.")

        try:
            quantity = float(quantity_str)
            unit_price = float(unit_price_str)
        except ValueError:
            abort(400, description="Quantity and unit price must be valid numbers.")

        if quantity <= 0 or unit_price < 0: # Unit price can be 0 for free items, quantity must be > 0
            abort(400, description="Quantity must be positive and unit price must be non-negative.")

        total_amount = quantity * unit_price
        current_transaction_id = next_sales_transaction_id

        new_sale = {
            "transaction_id": current_transaction_id, # Explicitly adding transaction_id
            "date": datetime.datetime.now(),
            "product_description": product_description,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
            "customer_info": customer_info,
            "payment_method": payment_method,
            "status": status,
            "recorded_by_user_id": 1,  # Placeholder user ID
            "comments": []
        }
        sales_transactions_db[current_transaction_id] = new_sale
        next_sales_transaction_id += 1

        # Assuming 'view_sale_detail' will be the function name for the transaction detail page
        return redirect(url_for('view_sale_detail', transaction_id=current_transaction_id))

    return render_template('log_sale.html')

@app.route('/sale/<int:transaction_id>')
def view_sale_detail(transaction_id):
    transaction_data = sales_transactions_db.get(transaction_id)
    if not transaction_data:
        abort(404)
    return render_template('sale_detail.html', transaction=transaction_data, transaction_id=transaction_id)

@app.route('/sale/<int:transaction_id>/add_comment', methods=['POST'])
def add_sale_comment(transaction_id):
    transaction_data = sales_transactions_db.get(transaction_id)
    if not transaction_data:
        abort(404)

    author_name = request.form.get('author_name')
    comment_text = request.form.get('comment_text')

    if not author_name or not comment_text:
        abort(400, description="Author name and comment text are required.")

    new_comment = {
        "author_name": author_name,
        "text": comment_text,
        "timestamp": datetime.datetime.now()
    }

    sales_transactions_db[transaction_id]['comments'].append(new_comment)

    return redirect(url_for('view_sale_detail', transaction_id=transaction_id))

# Banks Directory Routes
@app.route('/banks')
def view_banks_list():
    return render_template('banks_list.html', banks=banks_db)

@app.route('/banks/new', methods=['GET', 'POST'])
def add_new_bank():
    global next_bank_id
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        website_url = request.form.get('website_url', '')
        hq_location = request.form.get('hq_location', '')
        services_str = request.form.get('services', '')

        if not name:
            abort(400, description="Bank name is required.")

        services_list = [s.strip() for s in services_str.split(',') if s.strip()] if services_str else []

        current_id = next_bank_id
        new_bank = {
            "bank_id": current_id, # Explicitly adding bank_id
            "name": name,
            "description": description,
            "website_url": website_url,
            "hq_location": hq_location,
            "services": services_list,
            "comments": []
        }
        banks_db[current_id] = new_bank
        next_bank_id += 1

        # Assuming 'view_bank_detail' will be the function name for the bank detail page
        return redirect(url_for('view_bank_detail', bank_id=current_id))

    return render_template('add_bank.html')

@app.route('/bank/<int:bank_id>')
def view_bank_detail(bank_id):
    bank_data = banks_db.get(bank_id)
    if not bank_data:
        abort(404)
    return render_template('bank_detail.html', bank=bank_data, bank_id=bank_id)

@app.route('/bank/<int:bank_id>/add_comment', methods=['POST'])
def add_bank_comment(bank_id):
    bank_data = banks_db.get(bank_id)
    if not bank_data:
        abort(404)

    author_name = request.form.get('author_name')
    comment_text = request.form.get('comment_text')

    if not author_name or not comment_text:
        abort(400, description="Author name and comment text are required.")

    new_comment = {
        "author_name": author_name,
        "text": comment_text,
        "timestamp": datetime.datetime.now()
    }

    banks_db[bank_id]['comments'].append(new_comment)

    return redirect(url_for('view_bank_detail', bank_id=bank_id))

# Fintech Tools Directory Routes
@app.route('/fintech-tools')
def view_fintech_tools_list():
    return render_template('fintech_tools_list.html', fintech_tools=fintech_tools_db)

@app.route('/fintech-tools/new', methods=['GET', 'POST'])
def add_new_fintech_tool():
    global next_fintech_tool_id
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        website_url = request.form.get('website_url', '')
        category = request.form.get('category', '')
        pricing_model = request.form.get('pricing_model', '')

        if not name or not description:
            abort(400, description="Tool name and description are required.")

        current_id = next_fintech_tool_id
        new_tool = {
            "tool_id": current_id, # Explicitly adding tool_id
            "name": name,
            "description": description,
            "website_url": website_url,
            "category": category,
            "pricing_model": pricing_model,
            "comments": []
        }
        fintech_tools_db[current_id] = new_tool
        next_fintech_tool_id += 1

        # Assuming 'view_fintech_tool_detail' will be the function name for the tool detail page
        return redirect(url_for('view_fintech_tool_detail', tool_id=current_id))

    return render_template('add_fintech_tool.html')

@app.route('/fintech-tool/<int:tool_id>')
def view_fintech_tool_detail(tool_id):
    tool_data = fintech_tools_db.get(tool_id)
    if not tool_data:
        abort(404)
    return render_template('fintech_tool_detail.html', tool=tool_data, tool_id=tool_id)

@app.route('/fintech-tool/<int:tool_id>/add_comment', methods=['POST'])
def add_fintech_tool_comment(tool_id):
    tool_data = fintech_tools_db.get(tool_id)
    if not tool_data:
        abort(404)

    author_name = request.form.get('author_name')
    comment_text = request.form.get('comment_text')

    if not author_name or not comment_text:
        abort(400, description="Author name and comment text are required.")

    new_comment = {
        "author_name": author_name,
        "text": comment_text,
        "timestamp": datetime.datetime.now()
    }

    fintech_tools_db[tool_id]['comments'].append(new_comment)

    return redirect(url_for('view_fintech_tool_detail', tool_id=tool_id))

@app.route('/offline')
def offline_page():
    return render_template('offline.html')

@app.route('/sw.js')
def service_worker_route(): # Renamed function to avoid conflict if 'service_worker' is used elsewhere
    return send_from_directory(app.root_path, 'sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=True)
