from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from game_screen.utils.mongodb import session_collection
from game_screen.modules.game import list_game, get_game
from game_screen.modules.game_level import get_game_level
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from game_screen.utils.mongodb_utils import find_one_in_session
from game_screen.modules.game_category import get_game_category
from game_screen.utils.directus_utils import fetch_directus_user, create_directus_user, store_answer_in_directus
from game_screen.modules.game_utils import get_total_score, initialize_game_category, initialize_game_level, store_answer_in_mongodb

def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']

        # Check if user exists in Directus
        is_success, _, response = fetch_directus_user(username)
        if not is_success or (response.get('data') and len(response.get('data')) > 0):
            return render(request, 'register.html', {'error': 'Username already taken'})

        # Step 1: Hash password
        hashed_password = make_password(password)

        # Step 2: Send data to Directus
        body = {
            "name": name,
            "username": username,
            "password": hashed_password,
        }

        is_success, _, response = create_directus_user(body)

        print(response)

        if is_success:
            
            # Step 3: Use or create a Django User
            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.save()

            # Step 4: Authenticate and log in the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                return render(request, 'register.html', {'error': 'Authentication failed'})
        else:
            return render(request, 'register.html', {'error': 'Error creating user in Directus'})

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Use Django authenticate method
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect to homepage if login success
            return redirect('homepage')
        else:
            # If authentication fails, return an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

@login_required(login_url='/login/')
def homepage(request):
    session_id = request.session.get('session_id')
    session_data = find_one_in_session({"session_id": session_id})
    if session_data:
        name = session_data.get('name')
        return render(request, 'home.html', {'name': name})
    return render(request, 'home.html', {'error': 'No session data found'})

@login_required(login_url='/login/')
def select_game_category(request):
    data = get_game_category()
    if 'data' in data:
        session_id = request.session.get('session_id')
        total_score = get_total_score(session_id)
        return render(request, 'select_game_category.html', {'categories': data['data'], 'total_score': total_score})
    return render(request, 'error.html')

@login_required(login_url='/login/')
def select_game_level(request, game_category_id):
    data = get_game_level(game_category_id)
    if 'data' in data:
        session_id = request.session.get('session_id')
        total_score = get_total_score(session_id, game_category_id)
        initialize_game_category(session_id, game_category_id)
        return render(request, 'select_game_level.html', {'levels': data['data'], 'total_score': total_score})
    return render(request, 'error.html')

@login_required(login_url='/login/')
def select_game(request, game_category_id, game_level_id):
    data = list_game(game_level_id)
    if 'data' in data:
        session_id = request.session.get('session_id')
        total_score = get_total_score(session_id, game_category_id, game_level_id)
        initialize_game_level(session_id, game_level_id, game_level_id)
        param = {
            'games': data['data'], 
            'total_score': total_score, 
            'game_category_id': game_category_id
        }
        return render(request, 'select_game.html', param)
    return render(request, 'error.html')

@login_required(login_url='/login/')
def start_game(request, game_id):
    session_id = request.session.get('session_id')
    data = {}
    page = ""

    if not session_id:
        return render(request, 'error.html', {'error': 'Session not found'})

    response = get_game(game_id)
    if not 'data' in response:
        return render(request, "error.html")

    game = response["data"]
    game_category_id = game["game_level_id"]["game_category"]
    game_level_id = game["game_level_id"]["id"]
    session_data = find_one_in_session({"session_id": session_id})

    if not session_data:
        return render(request, 'home.html', {'error': 'No session data found'})

    player_id = session_data.get("directus_id")

    if request.method == "POST":
        answer = request.POST['answer']

        if game["game_type"] == "question_and_answer":
            correct_answer = game['correct_answer']
            is_correct = (answer.strip() == correct_answer.strip())
            score = game['score'] if is_correct else 0

            store_answer_in_mongodb(session_id, game_id, game_category_id, game_level_id, answer, score)
            store_answer_in_directus(game_id, player_id, None, answer, score, session_id)

            return redirect(f"/select-game/{game_category_id}/{game_level_id}")

        elif game["game_type"] == "select_an_option":
            correct_answer_option = game['correct_answer_option'][0]['answer_option_id']
            is_correct = (answer == correct_answer_option)
            score = game['score'] if is_correct else 0

            store_answer_in_mongodb(session_id, game_id, game_category_id, game_level_id, correct_answer_option, score)
            store_answer_in_directus(game_id, player_id, answer, None, score, session_id)

            return redirect(f"/select-game/{game_category_id}/{game_level_id}")

    else:
        page = ""
        if game["game_type"] == "question_and_answer":
            page = "start_game_input_answer.html"

        elif game["game_type"] == "select_an_option":
            page = "start_game_mcq.html"
        
        data = {"game": game}
        
    return render(request, page, data)

@login_required(login_url='/login/')
def logout_view(request):
    # Logout user, clear current session and store in history sessions
    session_id = request.session.get('session_id')

    if session_id:
        # Find the current session data in MongoDB
        session_data = session_collection.find_one({"session_id": session_id})

        if session_data:
            # append current session to history_sessions
            history_session = {
                "session_id": session_id,
                # login time of current session
                "login_time": session_data.get("login_time"),
                # store logout time
                "logout_time": datetime.now(),  
            }

            query = {"session_id": session_id}
            update = {
                "$push": {
                    "history_sessions": history_session
                },
                # remove current session_id and login time
                "$unset": {
                    "session_id": "",
                    "login_time": "" 
                }
            }

            # Update mongodb with the new history session
            session_collection.update_one(query, update)

    # Log the user out and redirect to login
    logout(request)
    return redirect('login')


