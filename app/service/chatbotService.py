from app.util.llmUtils import LLMUtils
from app.db.repository.eventRepo import EventRepository
import datetime

class ChatbotService:
    @staticmethod
    def process_query(query: str, db):
        """
        Process the user query, interact with the LLM, and execute commands.
        """
        llm_output = LLMUtils.generate_response_from_llm(query)
        return ChatbotService.execute_command(llm_output, db)

    @staticmethod
    def execute_command(command: str, db, ):
        """
        Execute the command returned by the LLM output.
        """
        if "getAllEvents()" in command:
            return EventRepository.get_all_events(db)
        elif "findEvent(" in command:
            date = datetime.now().date()
            return EventRepository.find_event_by_date(date, db)
        elif "findEventByVenue(" in command:
            venue_name = LLMUtils.extract_id_from_output(command, "findEventByVenue")
            return EventRepository.find_event_by_venue(venue_name, db)
        elif "getEventPrice(" in command:
            event_name = LLMUtils.extract_id_from_output(command, "getEventPrice")
            return EventRepository.get_event_price(event_name, db)
        elif "getEventDetails(" in command:
            event_name = LLMUtils.extract_id_from_output(command, "getEventDetails")
            return EventRepository.get_event_details(event_name, db)
        elif "findFreeEvents()" in command:
            return EventRepository.find_free_events(db)
        else:
            return {"error": "Command not recognized."}
