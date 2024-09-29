import requests
from bs4 import BeautifulSoup
def fetch_data(url):
    """Fetch document data and return it as a list of lines."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve document: {response.status_code}")

    # Parse the content and return the lines
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text("\n").strip().splitlines()


def parse_grid_data(data):
    """Extract grid data starting from the 'y-coordinate' section."""
    start_idx = data.index('y-coordinate') + 1  # Find the start of the actual data
    real_data = data[start_idx:]

    # Parse coordinates and characters into a dictionary
    char_positions = {
        (int(real_data[i].strip()), int(real_data[i + 2].strip())): real_data[i + 1]
        for i in range(0, len(real_data), 3)
    }
    return char_positions


def build_grid(char_positions):
    """Construct and return the grid from character positions."""
    max_x = max(pos[0] for pos in char_positions) + 1
    max_y = max(pos[1] for pos in char_positions) + 1
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]

    # Fill grid with characters
    for (x, y), char in char_positions.items():
        grid[y][x] = char

    return grid


def print_grid(grid):
    """Print the grid row by row."""
    for row in reversed(grid):
        print(''.join(row))


def retrieve_and_print_grid(url):
    """Fetch data, parse, build grid, and print."""
    data = fetch_data(url)
    char_positions = parse_grid_data(data)
    grid = build_grid(char_positions)
    print_grid(grid)


# Example usage
doc_url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
retrieve_and_print_grid(doc_url)