from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, random value

@app.route('/set_session')
def set_session():
    session['username'] = 'Nicola'
    return 'Session value set!'

@app.route('/get_session')
def get_session():
    username = session.get('username')
    if username:
        return f'Session value is: {username}'
    else:
        return 'No session value set!'

if __name__ == '__main__':
    app.run(debug=True)
