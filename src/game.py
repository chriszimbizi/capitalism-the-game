import random
from unidecode import unidecode
from data.comments import comments


def get_user_game_choice():
    """
    Gets the user's choice for how to play the game.

    Returns:
    - The user's choice as an integer.
    """
    while True:
        try:
            choice = int(
                input(
                    "\nHow would you like to play?\n\t1. Country of your choosing\n\t2. Random country\n\t3. Random country from a region of your choosing\n\t4. Exit\n "
                )
            )
            if 0 < choice < 5:
                return choice
            else:
                print("Please enter a number from 1 to 4.")
        except ValueError:
            print("Please enter a number from 1 to 4.")


def get_country(choice, all_countries_lower):
    """
    Gets the country based on the user's choice.

    Parameters:
    - choice (int): The user's choice.
    - all_countries_lower (list): List of lowercase country names.

    Returns:
    - The selected country name.
    """
    if choice == 1:  # User-inputted country
        while True:
            country_choice = input("\nChoose a country: ")
            country_choice = unidecode(country_choice.lower())

            if country_choice in all_countries_lower:
                return country_choice.title()
            else:
                country_choice = input("\nInvalid country. Enter a valid country: ")

    elif choice == 2:  # Random country
        return random.choice(all_countries_lower).title()

    elif choice == 3:  # Random country in user-chosen region
        region_mapping = {
            1: "africa",
            2: "americas",
            3: "asia",
            4: "europe",
            5: "oceania",
        }
        while True:
            try:
                region_choice = int(
                    input(
                        "\nChoose a region:\n\t1. Africa\n\t2. Americas\n\t3. Asia\n\t4. Europe\n\t5. Oceania\n"
                    )
                )
                if 0 < region_choice < 6:
                    region = region_mapping.get(region_choice)
                    break
                else:
                    print("Please enter a number from 1 to 5.")
            except ValueError:
                print("Please enter a number from 1 to 5.")

        if region:
            region_countries = get_region_countries(region)
            if region_countries:
                selected_country = random.choice(region_countries)
                return selected_country.title()
            else:
                print("Unable to retrieve the list of the region's countries.")


def play_game(country, capital):
    """
    Plays the game, prompting the user to guess the capital of the given country.

    Parameters:
    - country (str): The name of the country.
    - capital (str): The name of the capital city.
    """
    capital_processed = unidecode(capital.lower())

    while True:
        try:
            max_attempts = int(input("\nHow many guesses would you like? "))
            print()
            break
        except ValueError:
            print("Please enter a valid integer.")

    for attempt in range(1, max_attempts + 1):
        guess = input(
            f"Attempt {attempt}/{max_attempts}: What is the capital of {country}? 'f' to give up.\n\t"
        )
        guess_processed = unidecode(guess.lower())

        if not guess_processed:
            print("Invalid attempt, Please try again: ")

        elif guess_processed == capital_processed:
            print(
                f"\nWell done! You answered correctly. The capital city of {country} is {capital}."
            )
            break
        elif guess_processed[0] == "f":
            confirmation = input("\nAre you sure you want to give up? (y/n): ")
            if confirmation == "y":
                print(
                    f"I didn't peg you for a sore loser. The correct answer is {capital}.\n"
                )
                break
        elif attempt == max_attempts - 1:
            hint_prompt = input(
                "\nIncorrect. You have one more guess. Would you like a hint? (y/n): "
            )
            if hint_prompt.lower()[0] == "y":
                print(f"\nThe capital of {country} begins with {capital[0]}.")
                continue
            elif hint_prompt.lower()[0] == "n":
                print(f"\nAlright big shot, last chance.")
                continue
            else:
                hint_prompt = input("\nPlease enter 'y' or 'n': ")
        elif attempt == max_attempts:
            print(
                f"\nSorry, you've reached the maximum number of attempts. The correct answer is {capital}."
            )
        else:
            print(random.choice(comments))
            print()
