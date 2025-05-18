from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService
from validations.validations import get_input, is_email, none_word

auth = Authenticator(AuthService('database.db'))
        
username = get_input('Enter your username: ', none_word)
password = get_input('Enter your password: ', none_word)

user_login = auth.login(username, password)
print(user_login) # True

user_logout  = auth.logout()
print(user_logout) # True