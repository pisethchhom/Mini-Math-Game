from game_screen.utils.directus_integration import get_request

def list_game(game_level_id):
    # Query Game From Directus
    select_fields = [
        '*'
    ]

    # Select only published game and order by sort
    filter_q = f"&filter[game_level_id][_eq]={game_level_id}&filter[status][_eq]=published&sort[]=sort"

    [is_success, message, response] = get_request('game', select_fields, filter_q)

    if is_success:
        return response
    
    return {'error': message, 'response': response}

def get_game(game_id):
    select_fields = [
        '*',
        'game_level_id.*',
        'answer_option.*',
        'correct_answer_option.*'
    ]

    [is_success, message, response] = get_request(f"game/{game_id}", select_fields)

    if is_success:
        print(response)
        return response
    
    return {'error': message, 'response': response}