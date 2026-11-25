import json


def show_games():
    for game in games:
        print(f"ID: {game['id']}, Name: {game['name']}, Genre: {game['genre']}")

def add_game( name, genre):
    new_game = {
        "id": max(game['id'] for game in games) + 1 if games else 1,
        "name": name,
        "genre": genre
    }
    for game in games:
        if game['name'].lower() == name.lower() :
            print(f"Game '{name}' already exists.")
            return
    games.append(new_game)
    print(f"Game '{name}' added successfully.")
    save_games()

def find_game(id):
    for game in games:
        if game['id'] == id:
            return game
    print(f"Game with ID {id} not found.")

def delete_game(id):
    for game in games:
        if game['id'] == id:
            games.remove(game)
            save_games()
            print(f"Game with ID {id} deleted successfully.")
            return
    print(f"Game with ID {id} not found.")
    
def count_games():
    return len(games)

def filter_games_by_genre(genre):
    filtered_games = [game for game in games if game['genre'].lower() == genre.lower()]
    return filtered_games

def update_game(id, name=None, genre=None):
    for game in games:
        if game['id'] == id:
            if name is not None:
                game['name'] = name
            if genre is not None:
                game['genre'] = genre
            print(f"Game with ID {id} updated successfully.")
            return
    print(f"Game with ID {id} not found.")
    save_games()

def sort_games_by_name():
    return sorted(games, key=lambda x: x['name'])

def get_genre_statistics():
    genre_count = {}
    for game in games:
        get_genre = game['genre'].lower()
        if get_genre in genre_count:
            genre_count[get_genre] += 1
        else:
            genre_count[get_genre] = 1
    return genre_count
    
def sort_games_by_name():
    return sorted(games, key=lambda x: x['name'])

def load_games():
    with open("games.json", "r", encoding="utf-8") as file:
        return json.load(file)


def save_games():
    with open("games.json", "w", encoding="utf-8") as file:
        json.dump(games, file, ensure_ascii=False, indent=4)

games = load_games() 
        
def main():
    while True:
        print("\n=== GAME LIBRARY ===")
        print("1. Show games")
        print("2. Add game")
        print("3. Find game")
        print("4. Delete game")
        print("5. Update game")
        print("6. Filter by genre.")
        print("7. Genre statistics")
        print("8. Exit" )

        choice = input("Choose an option: ")

        if choice == "1":
            show_games()

        elif choice == "2":
            name = input("Game name: ")
            genre = input("Game genre: ")
            add_game(name, genre)

        elif choice == "3":
            game_id = int(input("Game ID: "))
            print(find_game(game_id))

        elif choice == "4":
            game_id = int(input("Game ID: "))
            delete_game(game_id)

        elif choice == "5":
            game_id = int(input("Game ID: "))
            name = input("New name (Enter to skip): ")
            genre = input("New genre (Enter to skip): ")

            update_game(
                game_id,
                name=name if name else None,
                genre=genre if genre else None
            )

        elif choice == "6":
            genre = input("Genre: ")
            print(filter_games_by_genre(genre))

        elif choice == "7":
            print(get_genre_statistics())

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


main()