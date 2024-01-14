from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from bson import json_util
from celery import Celery
import json
import redis

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://redistest-d7spia.serverless.use1.cache.amazonaws.com:6379:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redistest-d7spia.serverless.use1.cache.amazonaws.com:6379:6379/0'

# MongoDB Configuration
client = MongoClient("mongodb://127.0.0.1:27017/")  # Update the connection string accordingly
db = client["webhook_database"]
collection = db["webhooks"]

# Create Celery instance
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True, max_retries=3)
def fire_event_main(self, company_id, event_data):
    try:

        webhook = collection.find_one({"company_id": company_id, "is_active": True})

        if webhook:
            # Perform the webhook call
            response = post(webhook['url'], headers=webhook['headers'], json=event_data)
            response.raise_for_status()  # Raise an exception for HTTP errors

        else:
            print(f"No active webhook found for company_id: {company_id}")

    except Exception as exc:
        # Log the exception
        print(f"Webhook call failed: {exc}")

        # Retry the task with exponential backoff
        countdown = 2 ** self.request.retries
        self.retry(countdown=countdown)

#To create a webhook in the webhook_database
@app.route('/webhooks/', methods=['POST'])
def create_webhook():
    data = request.get_json()

    # Basic validation
    if not data or not all(key in data for key in ['company_id', 'url', 'events']):
        return jsonify({'error': 'Missing required fields'}), 400

    company_id = data['company_id']
    url = data['url']
    headers = data.get('headers', {})
    events = data['events']

    # Check if a webhook already exists for the given company_id and URL
    existing_webhook = collection.find_one({"company_id": company_id, "url": url})

    if existing_webhook:
        return jsonify({'error': 'Webhook already exists for the specified company_id and URL'}), 400

    # Create a new webhook subscription
    current_time = int(datetime.utcnow().timestamp())
    new_webhook = {
        'company_id': company_id,
        'url': url,
        'headers': headers,
        'events': events,
        'is_active': False,
        "created_at": current_time,
        "updated_at": current_time,
    }

    # Add the new webhook to the MongoDB collection
    collection.insert_one(new_webhook)

    return jsonify({'message': 'Webhook subscription created successfully'}), 201


# To update the webhook with the details for the company id
@app.route('/webhooks/<company_id>', methods=['PATCH'])
def update_webhook(company_id):
    data = request.get_json()

    # Set the updated_at timestamp
    data['updated_at'] = int(datetime.utcnow().timestamp())

    # Update the webhook subscription in the MongoDB collection
    result = collection.update_one({"company_id": company_id}, {"$set": data})

    if result.modified_count > 0:
        return jsonify({'message': 'Webhook subscription updated successfully'}), 200
    else:
        return jsonify({'error': 'Webhook subscription not found'}), 404

# To delete a webhook
@app.route('/webhooks/<company_id>', methods=['DELETE'])
def delete_webhook(company_id):
    # Delete the webhook subscription from the MongoDB collection
    result = collection.delete_one({"company_id": company_id})

    if result.deleted_count > 0:
        return jsonify({'message': 'Webhook subscription deleted successfully'}), 200
    else:
        return jsonify({'error': 'Webhook subscription not found'}), 404

# To get all the webhooks from the collections in webhook database
@app.route('/webhooks/', methods=['GET'])
def get_all_webhooks():
    # Get all webhooks from the MongoDB collection
    webhooks = list(collection.find())

    if not webhooks:
        return jsonify({'error': 'No webhooks found'}), 404

    # Convert ObjectId to string for JSON serialization
    serialized_webhooks = json.loads(json_util.dumps(webhooks))

    return jsonify(serialized_webhooks), 200

# To get the webhook of a particular company_id from the webhook database
@app.route('/webhooks/<company_id>', methods=['GET'])
def get_webhook(company_id):
    # Get the webhook subscription from the MongoDB collection
    webhook = collection.find_one({"company_id": company_id})

    if webhook:
        serialized_webhook = json.loads(json_util.dumps(webhook))
        return jsonify(serialized_webhook), 200
    else:
        return jsonify({'error': 'Webhook subscription not found'}), 404

# app.py

@app.route('/fire-event', methods=['POST'])
def fire_event():
    data = request.get_json()


    if not data or not all(key in data for key in ['company_id', 'event_data']):
        return jsonify({'error': 'Missing required fields'}), 400

    company_id = data['company_id']
    event_data = data['event_data']

    # Queue the Celery task to fire the event
    fire_event_main.apply_async(args=[company_id, event_data], countdown=0)

    return jsonify({'message': 'Event fired successfully'}), 200




if __name__ == '__main__':
    app.run(debug=True)
