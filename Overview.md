### Code Overview

This script utilizes the requests library to fetch content from a given Google Document and parses it using BeautifulSoup. The parsed text contains character positions, which are organized into a 2D grid based on x and y coordinates. The final output is a visual grid representation of these characters.

### Step-by-Step Explanation

1. **Importing Libraries**:

   ```python
   import requests
   from bs4 import BeautifulSoup
   ```

   - The necessary libraries are imported. requests is responsible for making HTTP requests to retrieve web content, while BeautifulSoup (from bs4) parses the HTML text from the document into usable data.

2. **Fetching Document Data**:

   ```python
   def fetch_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve document: {response.status_code}")
    return BeautifulSoup(response.text, 'html.parser').get_text("\n").strip().splitlines()
   ```

   - The fetch_data function retrieves the document from the provided URL. It checks if the request is successful (status code 200), then parses the content with BeautifulSoup. The parsed text is split into lines for easier processing.

3. **Parsing Grid Data**:

   ```python
   def parse_grid_data(data):
    start_idx = data.index('y-coordinate') + 1
    real_data = data[start_idx:]
    return {
        (int(real_data[i].strip()), int(real_data[i+2].strip())): real_data[i+1]
        for i in range(0, len(real_data), 3)
    }
   ```

   - This function begins by finding where the relevant data starts, just after the line labeled 'y-coordinate'. It then processes the data three lines at a time (x-coordinate, character, y-coordinate) and stores these as key-value pairs in a dictionary. The keys are tuples of x and y coordinates, and the values are the characters.

4. **Building the Grid**:

   ```python
   def build_grid(char_positions):
    max_x = max(pos[0] for pos in char_positions) + 1
    max_y = max(pos[1] for pos in char_positions) + 1
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]
    for (x, y), char in char_positions.items():
        grid[y][x] = char
    return grid
   ```

   - The build_grid function constructs a 2D list (grid) with dimensions based on the maximum x and y values in the char_positions dictionary. It initializes the grid with spaces and fills it with the appropriate characters based on the stored positions.

5. **Printing the Grid**:

   ```python
   def print_grid(grid):
    for row in reversed(grid):
        print(''.join(row))
   ```

   - This function simply prints the grid row by row. The reversed function ensures that the rows are displayed in the correct top-to-bottom order (as per Cartesian coordinates where y increases upwards).

6. **Main Function**:

   ```python
   def retrieve_and_print_grid(url):
    data = fetch_data(url)
    char_positions = parse_grid_data(data)
    grid = build_grid(char_positions)
    print_grid(grid)

   ```

   - This is the main function that ties everything together. It first fetches the document content, then parses the grid data, builds the 2D grid, and finally prints the resulting grid.

### Summary

The code retrieves character data from a Google Document, processes it into x, y coordinates, and builds a grid to display the characters in the correct positions. By breaking down the process into modular functions, the code is clean, efficient, and reusable.
