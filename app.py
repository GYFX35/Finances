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

# Job Postings Data Model
job_postings_db = {
    1: {
        "job_id": 1, # Explicitly adding for clarity, matches key
        "title": "Software Engineer, Backend",
        "company_name": "Tech Solutions Inc.",
        "location": "San Francisco, CA or Remote",
        "description": "Join our dynamic team to build next-generation web applications. We are looking for a skilled backend engineer passionate about technology.",
        "responsibilities": "- Design and implement scalable backend services.\n- Collaborate with frontend developers and product managers.\n- Write clean, maintainable, and testable code.",
        "qualifications": "- Bachelor's degree in Computer Science or related field.\n- 3+ years of experience in backend development.\n- Proficiency in Python and Django/Flask.",
        "employment_type": "Full-time",
        "how_to_apply": "Email your resume to careers@techsolutions.example.com",
        "salary_range": "$120,000 - $150,000 per year",
        "date_posted": datetime.datetime.now() - datetime.timedelta(days=2),
        "posted_by_user_id": 1, # Placeholder
        "comments": [
            {
                "author_name": "CandidateQuery",
                "text": "Is remote work open to international applicants?",
                "timestamp": datetime.datetime.now() - datetime.timedelta(days=1)
            }
        ]
    }
}
next_job_id = 2 # Since we added job 1

# News Items Data Model
news_items_db = {
    1: {
        "news_id": 1, # Explicitly adding for clarity, matches key
        "title": "Global Economic Outlook Brightens Slightly, Says Report",
        "source_name": "World Finance Monitor",
        "publication_date_str": "2023-10-25", # User input string for original pub date
        "summary": "A recent report from the World Finance Monitor indicates a slight improvement in the global economic outlook for the upcoming quarter, though significant regional disparities remain. Key factors include stabilizing energy prices and resilient consumer demand in several major economies.",
        "link_to_article": "http://example.com/news/global-outlook-oct23",
        "posted_by_user_id": 1, # Placeholder
        "date_posted_on_site": datetime.datetime.now() - datetime.timedelta(hours=10), # When it was added to this site
        "comments": [
            {
                "author_name": "EconAnalyst",
                "text": "Interesting take, but I think the regional disparities are more concerning than the report suggests.",
                "timestamp": datetime.datetime.now() - datetime.timedelta(hours=5)
            }
        ]
    }
}
next_news_id = 2 # Since we added news_id 1

# Global Chat Messages Data Model
chat_messages_db = [
    {
        "author_name": "Alice",
        "message_text": "Hello everyone! Welcome to the chat.",
        "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=10)
    },
    {
        "author_name": "Bob",
        "message_text": "Hi Alice! Glad to be here.",
        "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=5)
    },
    {
        "author_name": "Charlie",
        "message_text": "What's the topic of discussion today?",
        "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=1)
    }
]

# Esports Events Data Model
esports_events_db = {
    1: {
        "event_id": 1, # Explicitly adding for clarity
        "event_name": "Champions Tour Masters: Grand Final",
        "game_title": "Valorant",
        "event_datetime": datetime.datetime.now() + datetime.timedelta(days=7, hours=3), # Example: In 7 days and 3 hours
        "tournament_name": "VCT Masters Tokyo",
        "teams_involved": "Team Liquid vs Fnatic",
        "stream_link": "https://twitch.tv/valorant",
        "description": "The grand final of the Valorant Champions Tour Masters event in Tokyo.",
        "posted_by_user_id": 1, # Placeholder
        "date_posted_on_site": datetime.datetime.now() - datetime.timedelta(hours=2), # When it was added here
        "comments": [
            {
                "author_name": "ValorantFan1",
                "text": "This is going to be an epic match!",
                "timestamp": datetime.datetime.now() - datetime.timedelta(hours=1)
            }
        ]
    }
}
next_esports_event_id = 2 # Since we added event_id 1

# Dropshipping Suppliers Data Model
dropshipping_suppliers_db = {
    1: {
        "supplier_id": 1, # Explicitly adding for clarity
        "name": "Global Dropship Co.",
        "website_url": "http://globaldropshipco.example.com",
        "description": "Offers a wide range of consumer electronics and gadgets. Integrates with Shopify and WooCommerce. Ships from warehouses in Asia.",
        "product_niches": ["Electronics", "Gadgets", "Mobile Accessories"],
        "ships_from": "China, Vietnam",
        "ships_to": "Worldwide",
        "notes": "Good for starting out, wide product selection. Shipping times can vary.",
        "added_by_user_id": 1, # Placeholder
        "date_added": datetime.datetime.now() - datetime.timedelta(days=10),
        "comments": [
            {
                "author_name": "NewbieDropshipper",
                "text": "Has anyone used them for shipping to Europe? How are the delivery times?",
                "timestamp": datetime.datetime.now() - datetime.timedelta(days=1)
            }
        ]
    }
}
next_supplier_id = 2 # Since we added supplier_id 1

# Dropshipping Guides Data Model
dropshipping_guides_db = {
    1: {
        "guide_id": 1, # Explicitly adding for clarity
        "title": "Beginner's Guide to Finding Profitable Dropshipping Niches",
        "content": "Finding a profitable niche is crucial for dropshipping success...\n\nSection 1: Understanding Niches...\nSection 2: Market Research Techniques...\nSection 3: Validating Your Niche...",
        "author_name": "EcommercePro",
        "affiliate_link": "http://example.com/affiliate/dropship-guide-tool", # New field added
        "date_published": datetime.datetime.now() - datetime.timedelta(days=7),
        "last_updated": datetime.datetime.now() - datetime.timedelta(days=7),
        "comments": [
            {
                "author_name": "Learner101",
                "text": "This is super helpful, thanks for sharing!",
                "timestamp": datetime.datetime.now() - datetime.timedelta(days=2)
            }
        ]
    }
}
next_guide_id = 2 # Since we added guide_id 1

# Product Blogs Data Model
product_blogs_db = {
    1: {
        "post_id": 1, # Explicitly adding for clarity
        "title": "In-Depth Review: The SuperWidget X2000 for Dropshippers",
        "content": "The SuperWidget X2000 has been making waves in the dropshipping community...\n\n**Features:**\n- Feature A\n- Feature B\n\n**Pros:**\n- Pro 1\n- Pro 2\n\n**Cons:**\n- Con 1...",
        "author_name": "GadgetGuru",
        "product_name_focus": "SuperWidget X2000", # Optional field for the product name
        "affiliate_link": "http://example.com/affiliate/superwidgetx2000",
        "date_published": datetime.datetime.now() - datetime.timedelta(days=3),
        "last_updated": datetime.datetime.now() - datetime.timedelta(days=3),
        "comments": [
            {
                "author_name": "InterestedBuyer",
                "text": "Thanks for the review! Does it integrate well with platform Y?",
                "timestamp": datetime.datetime.now() - datetime.timedelta(days=1)
            }
        ]
    }
}
next_product_blog_post_id = 2 # Since we added post_id 1

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

# Job Postings Routes
@app.route('/jobs')
def view_jobs_list():
    # Sorting is handled in the template
    return render_template('jobs_list.html', jobs=job_postings_db)

@app.route('/jobs/post', methods=['GET', 'POST'])
def post_new_job():
    global next_job_id
    if request.method == 'POST':
        title = request.form.get('title')
        company_name = request.form.get('company_name')
        location = request.form.get('location')
        description = request.form.get('description')
        responsibilities = request.form.get('responsibilities', '')
        qualifications = request.form.get('qualifications', '')
        employment_type = request.form.get('employment_type', '')
        how_to_apply = request.form.get('how_to_apply')
        salary_range = request.form.get('salary_range', '')

        if not all([title, company_name, location, description, how_to_apply]):
            abort(400, description="Required fields are missing (Title, Company, Location, Description, How to Apply).")

        current_job_id = next_job_id
        new_job = {
            "job_id": current_job_id,
            "title": title,
            "company_name": company_name,
            "location": location,
            "description": description,
            "responsibilities": responsibilities,
            "qualifications": qualifications,
            "employment_type": employment_type,
            "how_to_apply": how_to_apply,
            "salary_range": salary_range if salary_range else "N/A",
            "date_posted": datetime.datetime.now(),
            "posted_by_user_id": 1,  # Placeholder
            "comments": []
        }
        job_postings_db[current_job_id] = new_job
        next_job_id += 1

        # Assuming 'view_job_detail' will be the function name for the job detail page
        return redirect(url_for('view_job_detail', job_id=current_job_id))

    return render_template('post_job.html')

@app.route('/job/<int:job_id>')
def view_job_detail(job_id):
    job_data = job_postings_db.get(job_id)
    if not job_data:
        abort(404)
    return render_template('job_detail.html', job=job_data, job_id=job_id)

@app.route('/job/<int:job_id>/add_comment', methods=['POST'])
def add_job_comment(job_id):
    job_data = job_postings_db.get(job_id)
    if not job_data:
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

    job_postings_db[job_id]['comments'].append(new_comment)

    return redirect(url_for('view_job_detail', job_id=job_id))

# News Item Routes
@app.route('/news')
def view_news_list():
    # Sorting is handled in the template
    return render_template('news_list.html', news_items=news_items_db)

@app.route('/news/post', methods=['GET', 'POST'])
def post_new_news_item():
    global next_news_id
    if request.method == 'POST':
        title = request.form.get('title')
        source_name = request.form.get('source_name')
        publication_date_str = request.form.get('publication_date_str', '') # Optional
        summary = request.form.get('summary')
        link_to_article = request.form.get('link_to_article', '') # Optional

        if not all([title, source_name, summary]):
            abort(400, description="Title, source name, and summary are required.")

        current_news_id = next_news_id
        new_item = {
            "news_id": current_news_id,
            "title": title,
            "source_name": source_name,
            "publication_date_str": publication_date_str if publication_date_str else "N/A",
            "summary": summary,
            "link_to_article": link_to_article if link_to_article else "",
            "posted_by_user_id": 1,  # Placeholder
            "date_posted_on_site": datetime.datetime.now(),
            "comments": []
        }
        news_items_db[current_news_id] = new_item
        next_news_id += 1

        # Assuming 'view_news_detail' will be the function name for the news detail page
        return redirect(url_for('view_news_detail', news_id=current_news_id))

    return render_template('post_news_item.html')

@app.route('/news/<int:news_id>')
def view_news_detail(news_id):
    item_data = news_items_db.get(news_id)
    if not item_data:
        abort(404)
    return render_template('news_detail.html', news_item=item_data, news_id=news_id)

@app.route('/news/<int:news_id>/add_comment', methods=['POST'])
def add_news_comment(news_id):
    item_data = news_items_db.get(news_id)
    if not item_data:
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

    news_items_db[news_id]['comments'].append(new_comment)

    return redirect(url_for('view_news_detail', news_id=news_id))

# Global Chat Page Route
@app.route('/chat', methods=['GET', 'POST'])
def global_chat_page():
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        message_text = request.form.get('message_text')

        if not author_name or not author_name.strip() or \
           not message_text or not message_text.strip():
            # In a real app, might flash a message instead of aborting
            abort(400, description="Author name and message text cannot be empty.")

        new_message = {
            "author_name": author_name,
            "message_text": message_text,
            "timestamp": datetime.datetime.now()
        }
        chat_messages_db.append(new_message)
        return redirect(url_for('global_chat_page'))

    # GET request: Display messages
    # Sort messages by timestamp, newest first for display
    sorted_messages = sorted(chat_messages_db, key=lambda x: x['timestamp'], reverse=True)
    return render_template('chat_page.html', messages=sorted_messages)

# Esports Event Routes
@app.route('/esports/schedule/new', methods=['GET', 'POST'])
def post_new_esports_event():
    global next_esports_event_id
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        game_title = request.form.get('game_title')
        event_date_str = request.form.get('event_date')
        event_time_str = request.form.get('event_time')
        event_timezone_str = request.form.get('event_timezone', '') # Optional
        tournament_name = request.form.get('tournament_name', '') # Optional
        teams_involved = request.form.get('teams_involved', '') # Optional
        stream_link = request.form.get('stream_link', '') # Optional
        description = request.form.get('description', '') # Optional

        if not all([event_name, game_title, event_date_str, event_time_str]):
            abort(400, description="Event name, game title, event date, and event time are required.")

        try:
            full_datetime_str = f"{event_date_str} {event_time_str}"
            event_dt_naive = datetime.datetime.strptime(full_datetime_str, '%Y-%m-%d %H:%M')
        except ValueError:
            abort(400, description="Invalid date or time format. Please use YYYY-MM-DD and HH:MM.")

        current_event_id = next_esports_event_id
        new_event = {
            "event_id": current_event_id,
            "event_name": event_name,
            "game_title": game_title,
            "event_datetime": event_dt_naive,
            "event_timezone_info": event_timezone_str if event_timezone_str else "Not specified",
            "tournament_name": tournament_name,
            "teams_involved": teams_involved,
            "stream_link": stream_link,
            "description": description,
            "posted_by_user_id": 1,  # Placeholder
            "date_posted_on_site": datetime.datetime.now(),
            "comments": []
        }
        esports_events_db[current_event_id] = new_event
        next_esports_event_id += 1

        # Assuming 'view_esports_event_detail' will be the function name
        return redirect(url_for('view_esports_event_detail', event_id=current_event_id))

    return render_template('post_esports_event.html')

@app.route('/esports/event/<int:event_id>')
def view_esports_event_detail(event_id):
    event_data = esports_events_db.get(event_id)
    if not event_data:
        abort(404)
    return render_template('esports_event_detail.html', event=event_data, event_id=event_id)

@app.route('/esports/event/<int:event_id>/add_comment', methods=['POST'])
def add_esports_event_comment(event_id):
    event_data = esports_events_db.get(event_id)
    if not event_data:
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

    esports_events_db[event_id]['comments'].append(new_comment)

    return redirect(url_for('view_esports_event_detail', event_id=event_id))

# Dropshipping Suppliers Directory Routes
@app.route('/dropshipping/suppliers')
def view_suppliers_list():
    # Sorting is handled in the template
    return render_template('suppliers_list.html', suppliers=dropshipping_suppliers_db)

@app.route('/dropshipping/suppliers/new', methods=['GET', 'POST'])
def add_new_supplier():
    global next_supplier_id
    if request.method == 'POST':
        name = request.form.get('name')
        website_url = request.form.get('website_url')
        description = request.form.get('description')
        product_niches_str = request.form.get('product_niches', '')
        ships_from = request.form.get('ships_from', '')
        ships_to = request.form.get('ships_to', '')
        notes = request.form.get('notes', '')

        if not all([name, website_url, description]):
            abort(400, description="Supplier name, website URL, and description are required.")

        product_niches_list = [n.strip() for n in product_niches_str.split(',') if n.strip()] if product_niches_str else []

        current_supplier_id = next_supplier_id
        new_supplier = {
            "supplier_id": current_supplier_id,
            "name": name,
            "website_url": website_url,
            "description": description,
            "product_niches": product_niches_list,
            "ships_from": ships_from if ships_from else "N/A",
            "ships_to": ships_to if ships_to else "N/A",
            "notes": notes,
            "added_by_user_id": 1,  # Placeholder
            "date_added": datetime.datetime.now(),
            "comments": []
        }
        dropshipping_suppliers_db[current_supplier_id] = new_supplier
        next_supplier_id += 1

        # Assuming 'view_supplier_detail' will be the function name
        return redirect(url_for('view_supplier_detail', supplier_id=current_supplier_id))

    return render_template('add_supplier.html')

@app.route('/dropshipping/supplier/<int:supplier_id>')
def view_supplier_detail(supplier_id):
    supplier_data = dropshipping_suppliers_db.get(supplier_id)
    if not supplier_data:
        abort(404)
    return render_template('supplier_detail.html', supplier=supplier_data, supplier_id=supplier_id)

@app.route('/dropshipping/supplier/<int:supplier_id>/add_comment', methods=['POST'])
def add_supplier_comment(supplier_id):
    supplier_data = dropshipping_suppliers_db.get(supplier_id)
    if not supplier_data:
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

    dropshipping_suppliers_db[supplier_id]['comments'].append(new_comment)

    return redirect(url_for('view_supplier_detail', supplier_id=supplier_id))

# Dropshipping Guides Routes
@app.route('/dropshipping/guides')
def view_guides_list():
    # Sorting is handled in the template
    return render_template('guides_list.html', guides=dropshipping_guides_db)

@app.route('/dropshipping/guides/new', methods=['GET', 'POST'])
def post_new_guide():
    global next_guide_id
    if request.method == 'POST':
        title = request.form.get('title')
        author_name = request.form.get('author_name')
        content = request.form.get('content')
        affiliate_link = request.form.get('affiliate_link', '') # Optional

        if not all([title, author_name, content]):
            abort(400, description="Title, author name, and content are required.")

        now = datetime.datetime.now()
        current_guide_id = next_guide_id

        new_guide = {
            "guide_id": current_guide_id,
            "title": title,
            "content": content,
            "author_name": author_name,
            "affiliate_link": affiliate_link if affiliate_link else "",
            "date_published": now,
            "last_updated": now, # Initially same as published
            "comments": []
        }
        dropshipping_guides_db[current_guide_id] = new_guide
        next_guide_id += 1

        # Assuming 'view_guide_detail' will be the function name
        return redirect(url_for('view_guide_detail', guide_id=current_guide_id))

    return render_template('post_guide.html')

@app.route('/dropshipping/guide/<int:guide_id>')
def view_guide_detail(guide_id):
    guide_data = dropshipping_guides_db.get(guide_id)
    if not guide_data:
        abort(404)
    return render_template('guide_detail.html', guide=guide_data, guide_id=guide_id)

@app.route('/dropshipping/guide/<int:guide_id>/add_comment', methods=['POST'])
def add_guide_comment(guide_id):
    guide_data = dropshipping_guides_db.get(guide_id)
    if not guide_data:
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

    dropshipping_guides_db[guide_id]['comments'].append(new_comment)

    return redirect(url_for('view_guide_detail', guide_id=guide_id))

# Product Blog Routes
@app.route('/products/blog')
def view_product_blogs_list():
    # Sorting is handled in the template
    return render_template('product_blogs_list.html', posts=product_blogs_db)

@app.route('/products/blog/new', methods=['GET', 'POST'])
def post_new_product_blog():
    global next_product_blog_post_id
    if request.method == 'POST':
        title = request.form.get('title')
        author_name = request.form.get('author_name')
        product_name_focus = request.form.get('product_name_focus', '') # Optional
        affiliate_link = request.form.get('affiliate_link', '') # Optional
        content = request.form.get('content')

        if not all([title, author_name, content]):
            abort(400, description="Title, author name, and content are required.")

        now = datetime.datetime.now()
        current_post_id = next_product_blog_post_id

        new_post = {
            "post_id": current_post_id,
            "title": title,
            "content": content,
            "author_name": author_name,
            "product_name_focus": product_name_focus if product_name_focus else "",
            "affiliate_link": affiliate_link if affiliate_link else "",
            "date_published": now,
            "last_updated": now, # Initially same as published
            "comments": []
        }
        product_blogs_db[current_post_id] = new_post
        next_product_blog_post_id += 1

        # Assuming 'view_product_blog_detail' will be the function name
        return redirect(url_for('view_product_blog_detail', post_id=current_post_id))

    return render_template('post_product_blog.html')

@app.route('/products/blog/post/<int:post_id>')
def view_product_blog_detail(post_id):
    post_data = product_blogs_db.get(post_id)
    if not post_data:
        abort(404)
    return render_template('product_blog_detail.html', post=post_data, post_id=post_id)

@app.route('/products/blog/post/<int:post_id>/add_comment', methods=['POST'])
def add_product_blog_comment(post_id):
    post_data = product_blogs_db.get(post_id)
    if not post_data:
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

    product_blogs_db[post_id]['comments'].append(new_comment)

    return redirect(url_for('view_product_blog_detail', post_id=post_id))

@app.route('/offline')
def offline_page():
    return render_template('offline.html')

@app.route('/sw.js')
def service_worker_route(): # Renamed function to avoid conflict if 'service_worker' is used elsewhere
    return send_from_directory(app.root_path, 'sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=True)
