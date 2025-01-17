import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

class LLMUtils:
    # Initialize the generative model as a class variable
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    @staticmethod
    def generate_response_from_llm(user_query: str) -> str:
        """
        Generate a response using the LLM for a given user query.
        """
        # Use LLMUtils.model instead of model
        response = LLMUtils.model.generate_content([
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

        return response.text

    @staticmethod
    def extract_id_from_output(output: str, function_name: str) -> str:
        """
        Extract the argument passed to the function in the LLM output.
        """
        start = output.find(function_name) + len(function_name) + 1
        end = output.find(")", start)
        return output[start:end].strip("\"")
