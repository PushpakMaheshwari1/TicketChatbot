TicketBot 
Welcome to TicketBot! This project is a backend API service for managing ticket bookings, providing functionalities for event listing, seat availability, and ticket booking through a chatbot interface.

Key Directories and Files:

    app/core/: Contains core utilities, such as database connection logic and security measures.
    app/db/: Holds database models (for events, venues, etc.), repositories for CRUD operations, and Pydantic schemas for validation.
    app/routers/: Contains route files for different parts of the application. chatbot.py contains routes for the chatbot API.
    app/service/: Contains service logic such as event, user, and venue management.
    app/util/: Utility files like initializing the database and interacting with the LLM (Large Language Model) for chatbot queries.
    main.py: Main entry point to launch the FastAPI application.

Installation Steps

1. Clone the repository:
First, clone the repository to your local machine:
  git clone https://github.com/yourusername/ticketBot.git
  cd ticketBot

2. Install the dependencies:
In your terminal, run the following command to install the required dependencies:
  pip3 install -r requirements.txt

3. Set up the database:
For this project, we are using PostgreSQL with Docker. Make sure you have Docker installed on your machine.
Start the PostgreSQL Docker container:
  docker-compose up
This will start the PostgreSQL container locally.

5. Run the application:
Now, start the FastAPI app by running:
  uvicorn main:app --reload

The API will be accessible at:
  http://127.0.0.1:8000/docs
You can access the interactive API documentation at the above URL to test your API endpoints.
