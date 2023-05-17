# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .features import productionShows,productionTable,regionalShows,regionalTable,querySearcher,question_formatter,extract_city,location_coder,openAiFunction

            

class timing_fetch(Action):

    def name(self) -> Text:
        return "action_movie_timing"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("$$$$$$$$$$$$$$$$$$$$$$","action_movie_timing")
            full_message = tracker.latest_message['text']
            broadway_show = tracker.get_slot("broadway_name")
            precityCode = tracker.get_slot("cityCode")
            city = extract_city(full_message)
            cityCode = location_coder(city)
            if precityCode == None and city == None:
                dispatcher.utter_message(text="in which location")
            elif cityCode == "('LN','WE','BR')" or cityCode =="('NY','OF','FF')":
                reply = productionTable(full_message,broadway_show,cityCode)
                dispatcher.utter_message(text=reply)
            else:
                reply = regionalTable(full_message,broadway_show)
                dispatcher.utter_message(text=reply)
            

            return []
        

class actionFacts(Action):
    def name(self) -> Text:
        return "action_about_facts"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_about_facts")
        try:
            full_message = tracker.latest_message['text']
            print(full_message)
            formated = question_formatter(full_message)
            print(formated)

            query = f'''SELECT answer FROM faq WHERE question = "{formated.strip()}";'''
            data = querySearcher(query)
            print(data)

            if len(data) == 0:
                response = f"sorry I don't have information about that"
            else:
                # Format show timings as a string
                response = ", ".join(str(result[0]) for result in data)
            
            dispatcher.utter_message(text=response)
            
            return []

        except:
            dispatcher.utter_message(text="sorry I didn't got your question")
            
            return []
        
class ActionSetMovieName(Action):
    def name(self) -> Text:
        return "action_movie"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_movie")
        full_message = tracker.latest_message['text']
        prompt_broadway = f"extract correct broadway name in the text\ntext: {full_message}\nreturn 'None' if there is no broadway show name present in text\ndo not add a single character by your side"
        broadway_show = openAiFunction(prompt_broadway)
        # prompt_city = f"Return the name of a city mentioned in the text, if any. If there is no city mentioned, return stripped 'None'. Do not perform any additional actions.\ntext: {full_message}"
        city = extract_city(full_message)
        if city == None and broadway_show == "None":
            return []
        elif city != None and broadway_show == "None":
            cityCode = location_coder(city)
            return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
        elif city==None:
           return [SlotSet("broadway_name", broadway_show)]
        else:
            cityCode = location_coder(city)
            return [SlotSet("broadway_name", broadway_show),SlotSet("place", city),SlotSet("cityCode", cityCode)]

class ActionSetCityName(Action):
    def name(self) -> Text:
        return "action_city"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_city")
        full_message = tracker.latest_message['text']
        city = extract_city(full_message)
        if city == None:
            return []
        cityCode = location_coder(city)
        return [SlotSet("place", city),SlotSet("cityCode",cityCode)]
    
class ActionSuggest(Action):
    def name(self) -> Text:
        return "action_suggest_show"

    async def run(
            self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_suggest_show")
        
        broadway_shows = tracker.get_slot("broadway_name")

        query = f'''SELECT prodtitle FROM productions WHERE tag = (SELECT tag FROM productions WHERE prodtitle = "{broadway_shows}" AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1) AND prodtitle != "{broadway_shows}" ORDER BY RAND() LIMIT 5;'''
        data = querySearcher(query)
        print(data)
        formatted_data = ", ".join([prod[0] for prod in data])
        dispatcher.utter_message(text=f"ya you must watch {formatted_data}")

        return []
class ActionAboutShow(Action):
    def name(self) -> Text:
        return "action_about_show"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_about_show")
        full_message = tracker.latest_message['text']
        broadway_show = tracker.get_slot("broadway_name")
        city = tracker.get_slot("place")
        cityCode = tracker.get_slot("cityCode")

        if cityCode == "('LN','WE','BR')" or cityCode =="('NY','OF','FF')":
            reply = productionTable(full_message,broadway_show,cityCode)
            dispatcher.utter_message(text=reply)
            return []
        else:
            reply = regionalTable(full_message,broadway_show)
            dispatcher.utter_message(text=reply)
            return []
    
class ActionSetName(Action):
    def name(self) -> Text:
        return "action_my_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_my_name")
        full_message = tracker.latest_message['text']
        prompt = f"just extract person's name from text\ntext: {full_message}"
        name = openAiFunction(prompt)
        
        dispatcher.utter_message(text=f"Hello {name}")

        return [SlotSet("username", name)]
    
# class ActionSetMovieTickets(Action):
#     def name(self) -> Text:
#         return "action_get_tickets"

#     async def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[Dict[Text, Any]]:
        
#         broadway_shows = tracker.get_slot("broadway_name")
#         location = tracker.get_slot("place")
#         cityCode = location_coder(location)
#         print(cityCode)
#         query = f'''SELECT tickets FROM productions WHERE prodtitle = "{broadway_shows}" AND market_type_code IN {cityCode};'''
#         data = querySearcher(query)

#         dispatcher.utter_message(text=f"This is the link for the tickets {data}")

#         return []





