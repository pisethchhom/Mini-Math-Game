from game_screen.utils.directus_integration import get_request

def get_game_level(game_category_id):
    # Query Game Level From Directus
    select_fields = [
        'id', 'title', 'short_description', 'game_category'
    ]
    
    # Select only published game and order by sort
    filter_q = f"&filter[game_category][_eq]={game_category_id}&filter[status][_eq]=published&sort[]=sort"

    [is_success, message, response] = get_request('game_level', select_fields, filter_q)

    print(response)
    if is_success:
        return response
    
    return {'error': message, 'response': response}

def get_game_level_by_id(game_level_id):
    # search directus game_level by id
    endpoint = f'game_level/{game_level_id}'
    [is_success, message, response] = get_request(endpoint, ['*'])

    if is_success:
        return {'data': response['data']}
    else:
        return {'error': message}
