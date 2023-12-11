from src.api import get_all_countries, get_country_capital
from src.game import get_user_game_choice, get_country, play_game
from src.utils import clear_screen


def main():
    all_countries_lower = get_all_countries()

    while True:
        clear_screen()
        print("\nWelcome to Capitalism!")
        game_choice = get_user_game_choice()

        if game_choice == 4:  # Quit
            confirmation = input("\nAre you sure you want to quit? (y/n): ")
            if confirmation == "y":
                print("Goodbye!\n")
                exit()
            else:
                game_choice = get_user_game_choice()

        country = get_country(game_choice, all_countries_lower)
        capital = get_country_capital(country)

        play_game(country, capital)

        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower()[0] != "y":
            confirmation = input("\nAre you sure you want to quit? (y/n): ")
            if confirmation == "y":
                print("Goodbye!\n")
                break


if __name__ == "__main__":
    main()
