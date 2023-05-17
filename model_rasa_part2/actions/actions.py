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
from .features import productionTable,regionalTable,querySearcher,question_formatter,location_coder,extraction_info,openFunction

            


            
        
class contextAction(Action):

    def name(self) -> Text:
        return "action_context_set"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("$$$$$$$$$$$$$$$$$$$$$$","action_context_set")

            full_message = tracker.latest_message['text']
            # prompt_broadway = f"I'm giving you a text which is basically a user's message searching about a local or broadway show so extract name of the show in the text\ntext: {full_message}\n only return show name or return None if show name is not specified in the text"
            both_info = extraction_info(full_message)
            broadway_show = both_info[0]
            pre_broadway_show = tracker.get_slot("broadway_name")
            preCity = tracker.get_slot("place")
            preCityCode = tracker.get_slot("cityCode")
            city = both_info[1]
            cityCode = location_coder(city)

            if broadway_show==None and city==None:
                print("###############  first condition worked")
                if pre_broadway_show==None and preCity==None:
                    dispatcher.utter_message(text="for which show and in which city")
                elif pre_broadway_show!=None and preCity==None:
                    #example : show runtime
                    try:
                        reply = regionalTable(full_message,pre_broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                        else:
                            dispatcher.utter_message(text="for which city")
                    except:
                        try:
                            reply = productionTable(full_message,pre_broadway_show,cityCode,city)
                            if len(reply)>1:
                                dispatcher.utter_message(text=reply)
                            else:
                                dispatcher.utter_message(text="for which city")
                        except:
                            dispatcher.utter_message(text="for which city")
                elif pre_broadway_show==None and preCity!=None:
                    if preCityCode == "('LN','WE')" or preCityCode =="('NY','OF','FF','BR')" or preCityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                       reply = productionTable(full_message,pre_broadway_show,preCityCode,preCity)
                       if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                       else:
                        try:
                            new_reply = regionalTable(full_message,pre_broadway_show,preCity)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                    else:
                        reply = regionalTable(full_message,broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                        else:
                            try:
                                new_reply = productionTable(full_message,broadway_show,preCityCode,preCity)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="sorry I don't have any data about this")
            
                else:
                    # when both are predefined
                    
                    if preCityCode == "('LN','WE')" or preCityCode =="('NY','OF','FF','BR')" or preCityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                       reply = productionTable(full_message,pre_broadway_show,preCityCode,preCity)
                       if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                       else:
                        try:
                            new_reply = regionalTable(full_message,pre_broadway_show,preCity)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                    else:
                        reply = regionalTable(full_message,pre_broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = productionTable(full_message,pre_broadway_show,preCityCode,preCity)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="sorry I don't have any data about this")

                       
            elif broadway_show!=None and city==None:
                print("############################  second condition worked")
                if preCity==None:
                    try:
                        reply = regionalTable(full_message,broadway_show,preCity)
                        dispatcher.utter_message(text=new_reply)
                    except:
                        try:
                            reply = productionTable(full_message,broadway_show,preCityCode,city)
                            dispatcher.utter_message(text=new_reply)
                        except:
                            dispatcher.utter_message(text="for which city")
                else:
                    if preCityCode == "('LN','WE')" or preCityCode =="('NY','OF','FF','BR')" or preCityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                       reply = productionTable(full_message,broadway_show,preCityCode,preCity)
                       if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                       else:
                        try:
                            new_reply = regionalTable(full_message,broadway_show,preCity)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                    else:
                        reply = regionalTable(full_message,broadway_show,preCity)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = productionTable(full_message,broadway_show,preCityCode,preCity)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="sorry I don't have any data about this")
                return [SlotSet("broadway_name", broadway_show)]

            elif broadway_show==None and city!=None:
                print("######################## third condition worked")
                if pre_broadway_show==None:
                    if cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')" or cityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                        reply = productionTable(full_message,broadway_show,cityCode,city)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = regionalTable(full_message,broadway_show,city)
                                dispatcher.utter_message(text=new_reply)
                                
                            except:
                                dispatcher.utter_message(text="for which show")
                                
                    else:
                        reply = regionalTable(full_message,broadway_show,city)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = productionTable(full_message,broadway_show,cityCode,city)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="for which show")
                else:
                    if cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')" or cityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                        reply = productionTable(full_message,pre_broadway_show,cityCode,city)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = regionalTable(full_message,pre_broadway_show,city)
                                dispatcher.utter_message(text=new_reply)
                                
                            except:
                                dispatcher.utter_message(text="for which show")
                                
                    else:
                        reply = regionalTable(full_message,pre_broadway_show,city)
                        if len(reply)>1:
                            dispatcher.utter_message(text=reply)
                            
                        else:
                            try:
                                new_reply = productionTable(full_message,pre_broadway_show,cityCode,city)
                                dispatcher.utter_message(text=new_reply)
            
                            except:
                                dispatcher.utter_message(text="for which show")
                return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
            else:
                print("last condition worked")
                if cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')" or cityCode in ["('LN')", "('WE')", "('BR')", "('NY')", "('OF')", "('FF')", "('LA')"]:
                    reply = productionTable(full_message,broadway_show,cityCode,city)
                    if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                    else:
                        try:
                            new_reply = regionalTable(full_message,broadway_show,city)
                            dispatcher.utter_message(text=new_reply)
                            
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                            
                else:
                    reply = regionalTable(full_message,broadway_show,city)
                    if len(reply)>1:
                        dispatcher.utter_message(text=reply)
                        
                    else:
                        try:
                            new_reply = productionTable(full_message,broadway_show,cityCode,city)
                            dispatcher.utter_message(text=new_reply)
        
                        except:
                            dispatcher.utter_message(text="sorry I don't have any data about this")
                return [SlotSet("broadway_name", broadway_show),SlotSet("place", city),SlotSet("cityCode", cityCode)]



        
        
class actionFacts(Action):
    def name(self) -> Text:
        return "action_about_facts"

    def run(self, dispatcher: CollectingDispatcher,
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
        
# class ActionSetMovieName(Action):
#     def name(self) -> Text:
#         return "action_movie"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[Dict[Text, Any]]:
#         print("$$$$$$$$$$$$$$$$$$$$$$","action_movie")
#         full_message = tracker.latest_message['text']
#         prompt_broadway = f"extract correct broadway name in the text\ntext: {full_message}\nreturn 'None' if there is no broadway show name present in text\ndo not add a single character by your side"
#         broadway_show = openAiFunction(prompt_broadway)
#         # prompt_city = f"Return the name of a city mentioned in the text, if any. If there is no city mentioned, return stripped 'None'. Do not perform any additional actions.\ntext: {full_message}"
#         city = extract_city(full_message)
#         if city == None and broadway_show == "None":
#             return []
#         elif city != None and broadway_show == "None":
#             cityCode = location_coder(city)
#             return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
#         elif city==None:
#            return [SlotSet("broadway_name", broadway_show)]
#         else:
#             cityCode = location_coder(city)
#             return [SlotSet("broadway_name", broadway_show),SlotSet("place", city),SlotSet("cityCode", cityCode)]

class ActionSetCityName(Action):
    def name(self) -> Text:
        return "action_city"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_city")
        full_message = tracker.latest_message['text']
        broadway_show = tracker.get_slot("broadway_name")
        city = extraction_info(full_message)[1]
        cityCode = location_coder(city)
        if city == None:
            dispatcher.utter_message(text="sorry I didn't got city can you ask again with show name and city name")
            return []
        elif cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')":
            reply = productionTable(full_message,broadway_show,cityCode,city)
            dispatcher.utter_message(text=reply)
            return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
        else:
            reply = regionalTable(full_message,broadway_show)
            dispatcher.utter_message(text=reply)
            return [SlotSet("place", city),SlotSet("cityCode", cityCode)]
        
    
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
# class ActionAboutShow(Action):
#     def name(self) -> Text:
#         return "action_about_show"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[Dict[Text, Any]]:
#         print("$$$$$$$$$$$$$$$$$$$$$$","action_about_show")
#         full_message = tracker.latest_message['text']
#         broadway_show = tracker.get_slot("broadway_name")
#         city = tracker.get_slot("place")
#         cityCode = tracker.get_slot("cityCode")

#         if cityCode == "('LN','WE')" or cityCode =="('NY','OF','FF','BR')":
#             reply = productionTable(full_message,broadway_show,cityCode)
#             dispatcher.utter_message(text=reply)
#             return []
#         else:
#             reply = regionalTable(full_message,broadway_show)
#             dispatcher.utter_message(text=reply)
#             return []
    
class ActionSetName(Action):
    def name(self) -> Text:
        return "action_my_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        print("$$$$$$$$$$$$$$$$$$$$$$","action_my_name")
        full_message = tracker.latest_message['text']
        prompt = f"just return person's name from text\ntext: {full_message}"
        name = openFunction(prompt)
        
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





