from game_screen.utils.directus_integration import get_request

def get_game_category():
    # Query Game Category From Directus
    select_fields = [
        'id', 'name', 'game_levels.id', 'game_levels.title' 
    ]

    # Select only published game and order by sort
    filter_q = f"&filter[status][_eq]=published&sort[]=sort"

    [is_success, message, response] = get_request('game_category', select_fields, filter_q)

    if is_success:
        return response
    
    return {'error': message, 'response': response}
