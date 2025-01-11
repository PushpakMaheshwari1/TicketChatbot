import os
import google.generativeai as genai
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.db.models.event import Event
from app.db.models import Venue
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Function to generate a response from the LLM
def generate_response_from_llm(user_query: str) -> str:
    """
    Generate a response using the LLM for a given user query.
    """
    response = model.generate_content([
        # Provide context for the model
        "input: List all today's events",
        "output: execute(findEvent(getDate()))",
        "input: What events are happening at Venue X?",
        "output: execute(findEventByVenue(X))",
        "input: Show me details for Event A",
        "output: execute(getEventDetails(A))",
        "input: How many seats are available for Event A",
        "output: execute(getSeatAvailability(A))",
        "input: Book a ticket for Event A",
        "output: execute(bookTicket(A, user_id))",
        "input: List all events this week",
        "output: execute(findEvent(getWeekDates()))",
        "input: Are there any free events",
        "output: execute(findFreeEvents())",
        "input: What's the price of Event A",
        "output: execute(getEventPrice(A))",
        "input: List events starting after 6 PM today",
        "output: execute(findEventsAfterTime(\"18:00\"))",
        "input: I want to book tickets for the Music Fest",
        "output: execute(finalize_ticket(X))",
        f"input: {user_query}",
        "output: ",
    ])

    print(f"User query: {user_query}")
    print(f"LLM response: {response.text}")
    return response.text


# Function to extract ID from the LLM response
def extract_id_from_output(output: str, function_name: str) -> str:
    """
    Extract the argument passed to the function in the LLM output.
    """
    start = output.find(function_name) + len(function_name) + 1
    end = output.find(")", start)
    return output[start:end].strip("\"")

# Function to execute commands returned by the LLM
def execute_command(command: str, db: Session, user_info: dict):
    """
    Parse and execute the command returned by the LLM output.
    """
    if "finalize_ticket(" in command:
        event_name = extract_id_from_output(command, "finalize_ticket")
        return collect_user_info(event_name, user_info)
    elif "execute(finalize_ticket(" in command:
        event_name = extract_id_from_output(command, "finalize_ticket")
        return collect_user_info(db, event_name, user_info)
    elif "getAllEvents()" in command:
        return get_all_events(db)
    elif "findEvent(" in command:
        date = datetime.now().date() 
        return findEvent(date, db)
    elif "findEventByVenue(" in command:
        venue_name = extract_id_from_output(command, "findEventByVenue")
        return find_event_by_venue(venue_name, db)
    elif "getEventPrice(" in command:
        event_name = extract_id_from_output(command, "getEventPrice")
        return get_event_price(event_name, db)
    elif "getEventDetails(" in command:
        event_name = extract_id_from_output(command, "getEventDetails")
        return get_event_details_by_name(event_name, db)
    elif "getSeatAvailability(" in command:
        event_name = extract_id_from_output(command, "getSeatAvailability")
        return get_seat_availability(event_name, db)
    elif "findFreeEvents()" in command:
        return find_free_events(db)
    else:
        return "Invalid command."


def handle_query(user_query: str, user_info: dict = None, db: Session = None) -> dict:
    """
    Process the user query, interact with the LLM, and collect necessary details.
    """
    if user_info is None:
        user_info = {}

    # Ensure user_info is a dictionary
    if not isinstance(user_info, dict):
        raise ValueError("user_info must be a dictionary.")

    # Generate LLM response
    llm_output = generate_response_from_llm(user_query)

    # Check if the user is responding to a prompt
    if "prompt" in user_info:
        key_to_update = user_info.pop("prompt_field", None)
        if key_to_update:
            user_info[key_to_update] = user_query
        else:
            return {"error": "Missing prompt field for user response."}

    # Execute command based on LLM output
    response = execute_command(llm_output, user_info)

    # Handle next prompt if required
    if "prompt" in response:
        return {
            "prompt": response["prompt"],
            "prompt_field": response.get("field", ""),
        }
    else:
        # Final response
        return {"response": response}

def collect_user_info(event_name: str, user_info: dict) -> dict:
    """
    Dynamically collect user information required for finalizing the ticket.
    """
    required_fields = ["name", "age", "seats"]  # Add other fields if needed
    
    # Check which fields are missing
    missing_fields = [field for field in required_fields if field not in user_info]

    if not missing_fields:
        # All required info is collected
        return finalize_ticket_process(event_name, user_info)

    # Ask for the next missing field
    next_field = missing_fields[0]

    if next_field == "name":
        return {"prompt": "Please provide your full name for the ticket."}
    elif next_field == "age":
        return {"prompt": "Please provide your age for the ticket."}
    elif next_field == "seats":
        return {"prompt": f"How many seats would you like to book for {event_name}?"}
    else:
        return {"prompt": "Please provide the required details."}

# Event-related functions
def findEvent(date: datetime, db: Session):
    today = datetime.now().date()
    events_today = db.query(Event).filter(Event.date == today).all()

    if not events_today:
        return "No events are happening today."

    return [
        {
            "event_name": event.name,
            "venue_id": event.venue_id,
            "date": event.date,
            "time": event.time,
            "available_seats": event.available_seats,
            "price": event.price,
        }
        for event in events_today
    ]


def get_all_events(db: Session):
    events = db.query(Event).all()
    return [
        {
            "event_name": event.name,
            "venue_id": event.venue_id,
            "date": event.date,
            "time": event.time,
            "available_seats": event.available_seats,
            "price": event.price,
        }
        for event in events
    ]

def get_event_price(event_name: str, db: Session):
    event = db.query(Event).filter(Event.name.ilike(f"%{event_name}%")).first()
    if event:
        return {
            "event_name": event.name,
            "price": event.price
        }
    else:
        return {"error": f"Sorry, no event found with the name '{event_name}'."}

def get_venue_id_from_name(venue_name: str, db: Session):
    venue = db.query(Venue).filter(Venue.name.ilike(f"%{venue_name}%")).first()
    return venue.id if venue else None


def find_event_by_venue(venue_name: str, db: Session):
    venue_id = get_venue_id_from_name(venue_name, db)
    if venue_id:
        events = db.query(Event).filter(Event.venue_id == venue_id).all()
        return [f"{event.name} on {event.date}" for event in events]
    return f"No venue found with the name {venue_name}."


def get_event_details_by_name(event_name: str, db: Session):
    event = db.query(Event).filter(Event.name.ilike(f"%{event_name}%")).first()
    return {
        "event_name": event.name,
        "date": event.date,
        "time": event.time,
        "price": event.price,
        "seats_available": event.available_seats,
    } if event else f"No details found for Event {event_name}."


def get_seat_availability(event_name: str, db: Session):
    event = db.query(Event).filter(Event.name.ilike(f"%{event_name}%")).first()
    return {
        "event_name": event.name,
        "seats_available": event.available_seats,
    } if event else f"No seat availability found for {event_name}."


def find_free_events(db: Session):
    free_events = db.query(Event).filter(Event.price == 0).all()
    return [f"{event.name} at {event.time}" for event in free_events] if free_events else "No free events available."

def finalize_ticket_process(event_name: str, user_info: dict) -> dict:
    """
    Generate the final ticket or bill once all user information is gathered.
    """
    # Simulate ticket details
    ticket_details = {
        "name": user_info["name"],
        "event_name": event_name,
        "age": user_info["age"],
        "seats": user_info["seats"],
        "total_price": 500 * int(user_info["seats"]),  # Example price calculation
    }

    # Here, you can generate a PDF using a library like `reportlab` or `weasyprint`
    return {
        "message": "Your ticket has been successfully booked!",
        "ticket_details": ticket_details,
    }


# Example query processing
def process_query(query: str, db: Session, user_info: dict):
    return handle_query(query, db, user_info)

