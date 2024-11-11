from game_screen.utils.directus_integration import post_request, get_request

def fetch_directus_user(username):
    filter_q = f"&filter[username][_eq]={username}"
    return get_request('player', ['*'], filter_q)

def create_directus_user(body):
    return post_request('player', body)

def store_answer_in_directus(game_id, player_id, selected_option, answer, score, session_id):
    data = {
        "player": player_id,
        "game": game_id,
        "selected_answer": selected_option,
        "answer": answer,
        "score": score,
        "session_id": session_id
    }

    print("@"*120)
    print(data)
    return post_request("progress_history", data)
