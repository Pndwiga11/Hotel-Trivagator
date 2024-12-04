# Hotel? Trivagator
Hotel Trivago is a project designed to generate personalized travel itineraries based on user preferences. It uses graph algorithms like Depth First Search (DFS) and Dijkstra's Algorithm to provide two different travel schedules.

## Features
- **Input**:
    - Destination, budget, duration, and interests.
- **Output**:
  - Two day-by-day itineraries with recommended destinations:
    - **DFS-Based Itinerary**: Explores paths comprehensively based on preferences.
    - **Dijkstra-Based Itinerary**: Provides the shortest path between locations.
  - **Graph Visualizations**: Interactive graphs highlighting realtive edges for DFS traversal and Dijkstra'a algorithm.

## Tools and Technologies
- **Python**: For data handling and algorithms
- **Flask**: For the web interface
- **Google Places API**: To fetch location data
- **NetworkX**: For graph representation
- **Pandas**: For dataset manipulation
- **Plotly**: For creating user-friendly graph visualizations.

## How to run the code
- Ensure **Python3.x** is installed.
- Install these Python libraries: Flask, NetworkX, Pandas, Plotly. Use this command: pip install Flask NetworkX Pandas Plotly
- Clone this repository.
- Navigate to project directory.
- Run the flask app with the command: python app.py
- Access the application in your browser with the link provided in the terminal, typically http://127.0.0.1:5000.

## Team Members
- Phillip Ndwiga
- Tess Jaworski
- Angela Luca
