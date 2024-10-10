from flask import Flask, session, request, jsonify, send_from_directory, jsonify, redirect, url_for
import json
from openai import OpenAI


app = Flask(__name__)
app.secret_key = 'akjfhafkjhajkbcja@'  # Replace with a strong, random value
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

def run():
  app.run(host='0.0.0.0')

client = OpenAI()

assistant = client.beta.assistants.retrieve("asst_rihv4yu9mdZ0hFQpnsZ1iWvH")

thread = client.beta.threads.create()
print(f"New chat session (thread) with ID: {thread.id}")

@app.route('/<path:path>')
def serve_static(path):
  # Serve file from public directory
  return send_from_directory('public', path)

@app.route('/')
def index():
  session['username'] = 'Nicola'
  print(f"session username: {session.get('username')}")
  return send_from_directory('public', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # Get message from request body
    data = json.loads(request.data)
    
    transcript = data['transcript']
    last_message = transcript[-1]["text"]

    username = session.get('username')
    if username:
        print(f'Session value is: {username}')
    else:
        print('No session value set!')
    
    message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=last_message
    )
    last_user_message_created_at = message.created_at
    
    modelrun = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
      # instructions="Please address the user as Nicola. The user has a premium account."
    )

    if modelrun.status == 'completed':
        # Fetch all messages and filter for the last message from the assistant
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
    
        # Filtering for assistant's messages
        assistant_messages = [msg for msg in messages.data if msg.role == 'assistant']
        if assistant_messages:
            for message in reversed(assistant_messages):
                # Access the 'created_at' attribute of each message
                if message.created_at > last_user_message_created_at:
                    # print the assistant message
                    last_assistant_message_text = message.content[0].text.value
                    print("\n")
                    print(f"Assistant: {last_assistant_message_text}")
                    print("\n")
                    return last_assistant_message_text
        else:
            print("No messages from the assistant.")
    else:
        print("Run status:", modelrun.status)

    # Return an error message if no response is available
    return jsonify({"error": "No response available"})