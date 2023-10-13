import pyrebase
from flask import flash, session, redirect, url_for
from typing import Tuple, Dict, Any, Optional

def initialize_firebase(config: Dict[str, str]) -> Tuple[Any, Any, Any, Any]:
    """
    Initialize Firebase with the given config.
    
    Usage:
        firebase, auth, db, storage = initialize_firebase(config)
    """
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
    storage = firebase.storage()
    
    return firebase, auth, db, storage

def create_user(email: str, password: str, auth: Any, db: Any) -> Any:
    """
    Register a new user with Firebase and store their data.

    Usage:
        response = create_user(email, password, auth, db)
    """
    try:
        user = auth.create_user_with_email_and_password(email, password)
        info = auth.get_account_info(user['idToken'])
        user_id = info['users'][0]['localId']
        session['uid'] = user_id

        user_data = {
            'id': user_id,
            'username': email,
            "device_id": '',
        }

        # Set or update user data in the Firebase Realtime Database
        db.child("users").child(user_id).child("user_data").set(user_data)

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            flash('The email address is already in use. Please use a different email or log in.', 'danger')
        else:
            flash('Error during registration. Please try again.', 'danger')
        return redirect(url_for('register'))

def login_user(username: str, password: str, auth: Any) -> Any:
    """
    Log in a user with Firebase.

    Usage:
        response = login_user(username, password, auth)
    """
    try:
        user = auth.sign_in_with_email_and_password(username, password)
        session['username'] = username
        info = auth.get_account_info(user['idToken'])
        user_id = info['users'][0]['localId']
        session['uid'] = user_id
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    except:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))

def get_user_data(user_uid: str, db: Any) -> Dict[str, Any]:
    """
    Retrieve user data from Firebase.
    
    Usage:
        user_data = get_user_data(user_uid, db)
    """
    return db.child("users").child(user_uid).get().val()

def update_user_data_in_db(user_uid: str, user_data: Dict[str, Any], db: Any) -> None:
    """
    Update user data in Firebase.

    Usage:
        update_user_data_in_db(user_uid, user_data, db)
    """
    db.child("users").child(user_uid).child("user_data").set(user_data)
