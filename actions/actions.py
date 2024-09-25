from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionConfirmReservation(Action):
    def name(self) -> Text:
        return "action_confirm_reservation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract entities
        date = tracker.get_slot('date')
        lieu = tracker.get_slot('lieu')

        # Format message
        message = f"Vous souhaitez réserver un hôtel pour le {date} à {lieu}, c'est bien ça ?"

        # Send message
        dispatcher.utter_message(text=message)

        return []
