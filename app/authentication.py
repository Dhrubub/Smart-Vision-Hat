import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyCQAj14X510dN2LreUiVJ-Ox26wqkR_xX8",
  'authDomain': "smart-vision-hat.firebaseapp.com",
  'projectId': "smart-vision-hat",
  'storageBucket': "smart-vision-hat.appspot.com",
  'messagingSenderId': "627181110284",
  'appId': "1:627181110284:web:deb55084063000eb565a29",
  'measurementId': "G-LL0X4KC7S6",
  'databaseURL': ''
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


email = 'test3@hotmail.com'
password = '123456'

# Create user
user = auth.create_user_with_email_and_password(email, password)
#print(user)
# Sign in
# user = auth.sign_in_with_email_and_password(email, password)

# Get user info
info = auth.get_account_info(user['idToken'])
print(info)

# # Send email verification
# auth.send_email_verification(user['idToken'])
# # Send password reset email
# auth.send_password_reset_email(email)

