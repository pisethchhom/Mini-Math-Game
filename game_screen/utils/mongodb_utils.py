from game_screen.utils.mongodb import session_collection

def find_one_in_session(query):
    return session_collection.find_one(query)

def update_session(query, update, array_filters=None):
    if array_filters:
        return session_collection.update_one(query, update, array_filters=array_filters)
    return session_collection.update_one(query, update)

def delete_session(session_id):
    session_collection.delete_one({"session_id": session_id})
