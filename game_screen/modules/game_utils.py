from datetime import datetime
from game_screen.utils.mongodb import session_collection

def get_total_score(session_id, game_category_id=None, game_level_id=None):
    # calculate user score and filter by category_id or level_id if provided
    query = {"session_id": session_id}

    # select all
    projection = {"game_category": 1}  

    # Fetch specific game category
    if game_category_id:
        query["game_category"] = {
            "$elemMatch": {
                "id": game_category_id
            }
        }
        projection = {
            "game_category.$": 1
        }

    result = session_collection.find_one(query, projection)
    total_score = 0

    print("+"*120)
    print(result)

    if result and 'game_category' in result:
        for category in result['game_category']:

            # Fetch specific game level if provide game_level_id
            if game_level_id:
                for level in category.get('game_level', []):
                    if level['id'] == game_level_id:
                        for game in level.get('game', []):
                            total_score += game.get('score', 0)
                        break
            else:
                # If no game_level_id is provided, calculate the total score for the whole category
                for level in category.get('game_level', []):
                    for game in level.get('game', []):
                        total_score += game.get('score', 0)
    
    return total_score

def initialize_game_category(session_id, game_category_id):
    # Add field game_category with empty game_level if not exist
    query = {"session_id": session_id}
    
    # Get current user session record
    result = session_collection.find_one(query)
    if result:
        #  check if the game_category already exists
        category_exists = any(category['id'] == game_category_id for category in result.get('game_category', []))

        if not category_exists:
            # Add a new game category
            new_category = {
                "id": game_category_id,
                "game_level": []
            }

            update = {
                "$push": {
                    "game_category": new_category
                }
            }

            session_collection.update_one(query, update)
            print("New game category initialized.")

def initialize_game_level(session_id, game_category_id, game_level_id):
    # Add field game_level with empty game if not exist
    query = {"session_id": session_id, "game_category.id": game_category_id}

    # Get current user session record
    result = session_collection.find_one(query)

    if result:
        for idx, category in enumerate(result.get('game_category', [])):
            if category['id'] == game_category_id:
                category = result['game_category'][idx]
                level_exists = any(level['id'] == game_level_id for level in category.get('game_level', []))
                if not level_exists:
                    # Add a new game level
                    new_level = {
                        "id": game_level_id,
                        "game": []
                    }

                    update = {
                        "$push": {
                            f"game_category.{idx}.game_level": new_level
                        }
                    }

                    session_collection.update_one(query, update)
                    print("New game level initialized.")
                break

def store_answer_in_mongodb(session_id, game_id, game_category_id, game_level_id, answer, score):
    # Get current user session record
    query = {"session_id": session_id}

    # Create the new game object with the answer and score
    new_game = {
        "id": game_id,
        "answer": answer,
        "score": score
    }

    # Find the current session data in MongoDB
    document = session_collection.find_one(query)

    if document:
        # Check if the game_category exists
        category_index = None
        for idx, category in enumerate(document.get('game_category', [])):
            if category['id'] == game_category_id:
                category_index = idx
                break

        if category_index is None:
            # Add new game category
            initialize_game_category(session_id, game_category_id)
            category_index = len(document.get('game_category', []))

        # Check if the game_level exists
        category = session_collection.find_one(query).get('game_category', [])[category_index]
        level_index = None
        for idx, level in enumerate(category.get('game_level', [])):
            if level['id'] == game_level_id:
                level_index = idx
                break

        if level_index is None:
            # Add new game level
            initialize_game_level(session_id, game_category_id, game_level_id)
            category = session_collection.find_one(query).get('game_category', [])[category_index]
            level_index = len(category.get('game_level', [])) - 1  # After initialization, it's the last one

        # Check if the game exists
        level = category.get('game_level', [])[level_index]
        game_index = None
        for idx, game in enumerate(level.get('game', [])):
            if game['id'] == game_id:
                game_index = idx
                break

        if game_index is not None:
            # Update existing game
            update = {
                "$set": {
                    f"game_category.{category_index}.game_level.{level_index}.game.{game_index}.answer": answer,
                    f"game_category.{category_index}.game_level.{level_index}.game.{game_index}.score": score
                }
            }
            session_collection.update_one(query, update)
            print("Game updated")
        else:
            # Add new game
            update = {
                "$push": {
                    f"game_category.{category_index}.game_level.{level_index}.game": new_game
                }
            }
            session_collection.update_one(query, update)
            print("Game added to existing level")
    else:
        # If no session exists, create a new document
        data = {
            "directus_id": document.get('directus_id'),  # Ensure you have access to this
            "session_id": session_id,
            "name": document.get('name'),
            "game_category": [
                {
                    "id": game_category_id,
                    "game_level": [
                        {
                            "id": game_level_id,
                            "game": [new_game]
                        }
                    ]
                }
            ],
            "login_time": datetime.now()
        }
        session_collection.insert_one(data)
        print("New session created and data inserted")
