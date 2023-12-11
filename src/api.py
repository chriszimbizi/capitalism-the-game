import requests


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
