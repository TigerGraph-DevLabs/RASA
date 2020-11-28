# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pyTigerGraph as tg

################# TigerGraph Credentials ######################""
configs = {
    "host": "https://<your_box>.i.tgcloud.io",
    "password": "<your_password>",
    "graphname": "<your_graph>",
    "secret" : "<your_secret>"
    }
#######################################"




################# TigerGraph Initialization ######################""
conn = tg.TigerGraphConnection(host=configs['host'], password=configs['password'], gsqlVersion="3.0.5", useCert=True, graphname=configs['graphname'])
conn.apiToken = conn.getToken(configs['secret'])
conn.gsql("USE graph {}".format(configs['graphname']))
#######################################"

class ActionSearchPatients(Action):

    def name(self) -> Text:
        return "action_search_patients"   # !!!! this return value must match line 55 of domain.yml  [ Step 4.a ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        print(tracker.latest_message)
        prediction = tracker.latest_message['entities'][0]['value']
        print("======================")
        print(prediction)
        print("======================")
        if prediction:
            query_response = conn.runInstalledQuery("listPatients_Infected_By",{"p": prediction})
            print(query_response)
            vals = query_response[0]["Infected_Patients"]
            value = ",".join(vals)
        
        counts = len(vals)
        if counts > 0:
            dispatcher.utter_message(template="utter_infection_source_filled",count=counts,patientid=value)
        else:
            dispatcher.utter_message(template="utter_infection_source_empty")

        return []



class ActionSearchPatientLocation(Action):

    def name(self) -> Text:
        return "action_patient_location"   # !!!! this return value must match line 56 of domain.yml  [ Step 4.a ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(tracker.latest_message)
        prediction = tracker.latest_message['entities'][0]['value']

        ###### TigerGraph Query #####################    
        places = ""
        print(prediction)
        if prediction:
            places = conn.gsql("select infection_case from Patient where patient_id == {} ".format(prediction))[0]["attributes"]['infection_case']

        if len(places) > 0:
            dispatcher.utter_message(template="utter_infection_place_filled",place=places,patientid=prediction)
        else:
            dispatcher.utter_message(template="utter_infection_place_empty")

        return []



class ActionSearchPokemon(Action):

    def name(self) -> Text:
        return "action_pokemon_type"   # !!!! this return value must match line 56 of domain.yml  [ Step 4.a ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        print(tracker.latest_message)
        prediction = tracker.latest_message['entities'][0]['value']
        places = ""
        if len(places) > 0:
            dispatcher.utter_message(template="utter_pokemon_filled",pokemontype=places,pokemonname=prediction)
        else:
            dispatcher.utter_message(template="utter_pokemon_empty",pokemonname=prediction)

        return []
