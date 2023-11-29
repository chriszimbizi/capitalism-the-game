import requests
import random
from unidecode import unidecode

# List of comments for incorrect answers
comments = [
    "Come on, you can do better!",
    "Seriously? Try again!",
    "Wow, that was way off!",
    "Nice try, but not quite.",
    "Keep guessing!",
    "Is that the best you've got?",
    "Almost there, but not quite!",
    "A for effort, F for results!",
    "Not even close!",
    "Haha, not even in the ballpark!",
    "Give it another shot, maybe you'll get lucky!",
    "You're about as accurate as a blindfolded archer!",
    "Fail to the chief! Try again.",
    "You must be a master of almost getting it right!",
    "Next time, perhaps?",
    "Are you sure you're trying?",
    "One small step for you, one giant leap for failure!",
    "I've seen better attempts in my sleep!",
    "You're like a broken compass, all over the place!",
]


def api_request(url, return_type=None):
    """
    Makes an API request to the given URL and processes the data using the specified return type.

    Parameters:
    - url (str): The URL to make the API request.
    - return_type (function): A function to process the data. If None, returns raw data.

    Returns:
    - The processed data or raw data if no return_type is specified.
    """
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            return data if return_type is None else return_type(data)
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_all_countries():
    """
    Gets a list of all countries, processing the data to return lowercase names.

    Returns:
    - A list of lowercase country names.
    """
    return api_request(
        "https://restcountries.com/v3.1/all",
        lambda data: [country["name"]["common"].lower() for country in data],
    )


def get_region_countries(region):
    """
    Gets a list of countries in the specified region, processing the data to return lowercase names.

    Parameters:
    - region (str): The region for which to get countries.

    Returns:
    - A list of lowercase country names in the specified region.
    """
    return api_request(
        f"https://restcountries.com/v3.1/region/{region}",
        lambda data: [country["name"]["common"].lower() for country in data],
    )


def get_country_capital(country_name):
    """
    Gets the capital of the specified country.

    Parameters:
    - country_name (str): The name of the country.

    Returns:
    - The capital of the specified country.
    """
    return api_request(
        f"https://restcountries.com/v3.1/name/{country_name}",
        lambda data: data[0].get("capital", ["Unknown"])[0],
    )


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
            break
        except ValueError:
            print("Please enter a valid integer.")

    for attempt in range(1, max_attempts + 1):
        guess = input(
            f"\nAttempt {attempt}/{max_attempts}: What is the capital of {country}? 'f' to give up.\n\t"
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
        elif attempt == max_attempts:
            print(
                f"Sorry, you've reached the maximum number of attempts. The correct answer is {capital}.\n"
            )
        else:
            print(random.choice(comments))


if __name__ == "__main__":
    all_countries_lower = get_all_countries()

    print("\nWelcome to Capitalism!")

    while True:
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
