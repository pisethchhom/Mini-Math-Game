import uuid
import requests
from datetime import datetime
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from game_screen.utils.directus_integration import get_request, patch_request
from game_screen.utils.mongodb import session_collection

class DirectusBackend(BaseBackend):
    # Authenticate using Directus Player Model
    def authenticate(self, request, username=None, password=None):
        try:
            # Step 1: Fetch user data from Directus using Directus API
            filter_q = f"&filter[username][_eq]={username}"
            [is_success, message, response] = get_request('player', ['*'], filter_q)

            if not is_success:
                return None

            user_data = response.get('data')

            # Step 2: Validate if the user exists in Directus
            if user_data and len(user_data) > 0:
                directus_user = user_data[0]  # Assuming only one result is returned
                directus_password = directus_user['password']  # Password from Directus (hashed)

                # Step 3: Check the password with Django's check_password function
                if check_password(password, directus_password):
                    # Step 4: Try to find the user in Django's local User model
                    try:
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        # Step 5: Create the user in Django if it does not exist
                        user = User(username=username)
                        user.set_unusable_password()  # Disable password in Django since Directus handles it
                        user.save()

                    # Generate a new session ID
                    new_session_id = str(uuid.uuid4())

                    # Step 6: Search for the existing MongoDB record using directus_id
                    existing_session = session_collection.find_one({"directus_id": directus_user.get('id')})

                    if existing_session:
                        # Update the session_id and login_time for the existing session
                        update = {
                            "$set": {
                                "session_id": new_session_id,  # Update session_id to the new one
                                "login_time": datetime.now()  # Update the login time
                            }
                        }
                        session_collection.update_one({"directus_id": directus_user.get('id')}, update)
                    else:
                        # If no existing session is found, create a new session record
                        data = {
                            "directus_id": directus_user.get('id'),
                            "session_id": new_session_id,
                            "name": directus_user.get('name'),
                            "game_category": [],  # Game data, if needed, can be updated later
                            "login_time": datetime.now()  # Track the login time
                        }
                        session_collection.insert_one(data)

                    # Step 7: Store the session ID in Django's session
                    request.session['session_id'] = new_session_id

                    # Step 8: Update Directus with the last login time
                    player = f"player/{directus_user.get('id')}"
                    update_body = {"last_login_at": datetime.now().isoformat()}
                    patch_request(player, update_body)

                    return user

        except requests.RequestException as e:
            print(f"Error fetching user from Directus: {e}")

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
