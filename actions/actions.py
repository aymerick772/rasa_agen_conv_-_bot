import logging
import random
import string
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Configurer le logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ActionListChoice(Action):
    def name(self) -> Text:
        return "action_list_choice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        logger.info("ActionListChoice: Listing choices for the user.")
        dispatcher.utter_message(text="""Que souhaitez-vous faire ?
1. Nouvelle réservation
2. Annuler une réservation
3. Information sur une réservation
4. Voir le menu du jour
5. Consulter la liste des allergènes
6. Accéder à notre carte complète""")
        return []

class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        date = tracker.get_slot("date")
        people = tracker.get_slot("people")
        logger.info(f"ActionCheckAvailability: Checking availability for {people} people on {date}.")
        
        # Simulation de disponibilité (à remplacer par vraie logique)
        available = True
        logger.info(f"ActionCheckAvailability: Availability result: {available}.")
        
        if available:
            dispatcher.utter_message(text=f"Une table pour {people} personne(s) est disponible le {date}.")
            logger.info("ActionCheckAvailability: Availability confirmed.")
            return [SlotSet("availability_checked", True)]
        else:
            dispatcher.utter_message(text=f"Désolé, aucune table n'est disponible pour {people} personne(s) le {date}. Souhaitez-vous essayer une autre date ?")
            logger.info("ActionCheckAvailability: No availability.")
            return [SlotSet("availability_checked", False)]

class ActionGenerateReservationCode(Action):
    logger.info(f"IIIIRENTRLA.")
    def name(self) -> Text:
        return "action_generate_reservation_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Générer un code aléatoire
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        logger.info(f"ActionGenerateReservationCode: Generated reservation code: {code}.")
        
        dispatcher.utter_message(text=f"Votre code de réservation est : {code}. Gardez-le précieusement, il vous sera demandé pour toute modification ou annulation.")
        return [SlotSet("reservation_code", code)]

class ActionAddComment(Action):
    def name(self) -> Text:
        return "action_add_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        comment = tracker.latest_message.get("text")
        code = tracker.get_slot("reservation_code")
        logger.info(f"ActionAddComment: Adding comment to reservation {code}. Comment: {comment}")
        
        # Simulation d'ajout de commentaire
        dispatcher.utter_message(text=f"Commentaire ajouté à la réservation {code} : {comment}")
        return []

class ActionValidateReservationCode(Action):
    def name(self) -> Text:
        return "action_validate_reservation_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        code = tracker.get_slot("reservation_code")
        logger.info(f"ActionValidateReservationCode: Validating code: {code}")
        
        # Simulation de validation (à remplacer par vraie logique)
        if code and len(code) == 6:
            logger.info("ActionValidateReservationCode: Code is valid.")
            return [SlotSet("code_valid", True)]
        else:
            dispatcher.utter_message(text="Code de réservation invalide. Veuillez réessayer.")
            logger.info("ActionValidateReservationCode: Code is invalid.")
            return [SlotSet("code_valid", False)]

class ActionGetReservationInfo(Action):
    def name(self) -> Text:
        return "action_get_reservation_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        code = tracker.get_slot("reservation_code")
        logger.info(f"ActionGetReservationInfo: Fetching information for reservation code: {code}")
        
        # Simulation d'information (à remplacer par vraie logique)
        if code:
            dispatcher.utter_message(text=f"""Informations de réservation pour le code {code}:
- Date: {tracker.get_slot('date')}
- Personnes: {tracker.get_slot('people')}
- Nom: {tracker.get_slot('name')}
- Téléphone: {tracker.get_slot('phone')}""")
            logger.info("ActionGetReservationInfo: Reservation information sent.")
        else:
            logger.info("ActionGetReservationInfo: No reservation code found.")
        return []

class ActionCancelReservation(Action):
    def name(self) -> Text:
        return "action_cancel_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        code = tracker.get_slot("reservation_code")
        logger.info(f"ActionCancelReservation: Attempting to cancel reservation with code: {code}")
        
        if tracker.get_slot("code_valid"):
            dispatcher.utter_message(text=f"La réservation {code} a été annulée avec succès.")
            logger.info("ActionCancelReservation: Reservation cancelled successfully.")
            return [SlotSet("reservation_code", None)]
        else:
            dispatcher.utter_message(text="Impossible d'annuler la réservation. Code invalide.")
            logger.info("ActionCancelReservation: Cancellation failed. Invalid code.")
            return []
