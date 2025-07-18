# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ActiveLoop, EventType
import requests
import re
import os
import subprocess
import json
from datetime import datetime, timedelta
from langdetect import detect
from langdetect import detect, LangDetectException
# from rasa_sdk.events import FollowupAction
# from rasa_sdk.events import UserUttered


# # -------- Movie Recommendation (based on actor only) --------
# class ActionRecommendMovie(Action):

#     def name(self) -> Text:
#         return "action_recommend_movie"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         actor = tracker.get_slot("actor")
#         api_key = "452d3f827f883c3dea7593abcc047e34"  # TMDb API Key

#         if not actor:
#             dispatcher.utter_message(text="Please provide an actor's name.")
#             return []

#         try:
#             # Step 1: Get Actor ID
#             search_url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor}"
#             actor_data = requests.get(search_url).json().get("results", [])
#             if not actor_data:
#                 dispatcher.utter_message(text=f"❌ No actor found with name '{actor}'.")
#                 return []

#             actor_id = actor_data[0]["id"]

#             # Step 2: Get Actor's Movies
#             movie_url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={api_key}"
#             movies = requests.get(movie_url).json().get("cast", [])

#             if not movies:
#                 dispatcher.utter_message(text=f"❌ No movies found for {actor}.")
#                 return []

#             # Step 3: Pick top movie
#             top_movie = sorted(movies, key=lambda x: x.get("popularity", 0), reverse=True)[0]
#             title = top_movie.get("title", "Unknown Title")
#             overview = top_movie.get("overview", "No description available.")

#             dispatcher.utter_message(text=f"🎬 You might enjoy *{title}*.\n📝 {overview}")
#         except Exception as e:
#             dispatcher.utter_message(text=f"⚠️ Error fetching movie: {str(e)}")

#         return []

# # -------- Weather Info (based on city) --------
# class ActionGetWeather(Action):

#     def name(self) -> Text:
#         return "action_get_weather"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         city = tracker.get_slot("city")
#         api_key = "0916c53321cb61ca6d84cbf6d7622df2"  # Replace with your API key

#         if not city:
#             dispatcher.utter_message(text="Please provide a city name.")
#             return []

#         try:
#             weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#             response = requests.get(weather_url).json()

#             if response.get("cod") != 200:
#                 dispatcher.utter_message(text=f"❌ Couldn't get weather for '{city}'.")
#                 return []

#             temp = response["main"]["temp"]
#             desc = response["weather"][0]["description"]
#             dispatcher.utter_message(text=f"🌤️ The weather in {city} is {desc} with a temperature of {temp}°C.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"⚠️ Error getting weather: {str(e)}")

#         return []
# # Date and Time:
# class ActionProvideDate(Action):
#     def name(self) -> Text:
#         return "action_provide_date"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_message = tracker.latest_message.get("text", "").lower()
#         today = datetime.now().date()

#         offset = 0
#         match = re.search(r'(\d+)\s+days?\s+(ago|later|from now)', user_message)
#         if "yesterday" in user_message:
#             offset = -1
#         elif "tomorrow" in user_message:
#             offset = 1
#         elif match:
#             number = int(match.group(1))
#             direction = match.group(2)
#             offset = -number if direction == "ago" else number

#         result_date = today + timedelta(days=offset)
#         dispatcher.utter_message(text=f"The date is {result_date.strftime('%A, %d %B %Y')}")
#         return []

# class ActionProvideTime(Action):
#     def name(self) -> Text:
#         return "action_provide_time"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_message = tracker.latest_message.get("text", "").lower()
#         now = datetime.now()

#         offset = 0
#         match = re.search(r'(\d+)\s+hours?\s+(ago|later|from now)', user_message)
#         if match:
#             number = int(match.group(1))
#             direction = match.group(2)
#             offset = -number if direction == "ago" else number

#         result_time = now + timedelta(hours=offset)
#         dispatcher.utter_message(text=f"The time is {result_time.strftime('%I:%M %p')}")
#         return []
 
# Ollama LLM

# class ActionLlamaResponse(Action):
#     def name(self) -> Text:
#         return "action_llama_response"

#     def run(self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_input = tracker.latest_message.get("text")
        
#         # Prepare the payload for Ollama's chat API
#         payload = {
#             "model": "llama3.2:latest",
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": user_input
#                 }
#             ],
#             "stream": False  # Important for getting full answer in one response
#         }

#         try:
#             response = requests.post("http://localhost:11434/api/chat", json=payload)
#             response.raise_for_status()
#             bot_reply = response.json()["message"]["content"]
#         except Exception as e:
#             bot_reply = f"⚠️ Error communicating with LLaMA model: {str(e)}"

#         dispatcher.utter_message(text=bot_reply)
#         return []

class ValidateAwbForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_awb_form"

    def validate_awb_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        language = tracker.get_slot("language1")
        
        if slot_value.isdigit() and len(slot_value) == 7:
            return {"awb_number": slot_value}  # <-- Check your slot name here
        else:
            if language == "hindi":
                dispatcher.utter_message(text=f"❌ '{slot_value}' एक मान्य ७-अंकीय संख्या नहीं है। कृपया पुनः प्रयास करें।")
            else:
                dispatcher.utter_message(text=f"❌ '{slot_value}' is not a valid 7-digit AWB number. Please try again.")
            return {"awb_number": None}   

class ActionStoreRating(Action):

    def name(self) -> str:
        return "action_store_rating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        language = tracker.get_slot("language1") 

        rating = tracker.get_slot("rating_value")
        user_id = tracker.sender_id
        timestamp = datetime.now().isoformat()

       # Log it (can be replaced with DB/Google Sheet etc.)
        # print(f"[Rating] User: {user_id} | Rating: {rating} | Time: {timestamp}")
        
        # Debug message
        # dispatcher.utter_message(text=f"Thanks for rating us {rating} stars!")
        # You can also store this to a file or DB
        with open("ratings_log.txt", "a") as f:
            f.write(f"{timestamp} | User: {user_id} | Rating: {rating}\n")
        
        if language == "hindi":
            dispatcher.utter_message(text=f"🙏 हमारे सेवा का उपयोग करने के लिए धन्यवाद। हम आपकी प्रतिक्रिया की सराहना करते हैं। आपका दिन शुभ हो! 👋")
        else:
            dispatcher.utter_message(text=f"Thank you for using our service. We appreciate your feedback. Have a great day! 👋")
                
        
        
        return []    

class ActionShowOffers(Action):
    def name(self) -> Text:
        return "action_show_offers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language1")

        if language == "hindi":
            dispatcher.utter_message(text="ज़रूर, नीचे सभी चालू ऑफ़र दिए गए हैं। सभी ऑफ़र्स देखने के लिए स्लाइड करें:")

            carousel = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "एक्सप्रेस शिपमेंट पर 50% की छूट",
                            "subtitle": "सीमित समय की पेशकश",
                            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqhmyBRCngkU_OKSL6gBQxCSH-cufgmZwb2w&usqp=CAU",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "अभी पाएं",
                                    "payload": "/express_offer"
                                }
                            ]
                        },
                        {
                            "title": "नेक्स्ट-डे डिलीवरी पर ₹100 की छूट",
                            "subtitle": "15 जुलाई तक मान्य",
                            "image_url": "https://image.freepik.com/free-vector/city-illustration_23-2147514701.jpg",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "बुक करें",
                                    "payload": "/next_day_offer"
                                }
                            ]
                        },
                        {
                            "title": "प्रीमियम यूज़र्स के लिए फ्री ट्रैकिंग",
                            "subtitle": "बिना किसी शुल्क के ट्रैक करें",
                            "image_url": "https://img.freepik.com/free-vector/delivery-concept-illustration_114360-5000.jpg",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "और जानें",
                                    "payload": "/tracking_offer"
                                }
                            ]
                        }
                    ]
                }
            }

        else:
            dispatcher.utter_message(text="Sure, below are the ongoing offers. Slide the images to see all:")

            carousel = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "50% Off on Express Shipments",
                            "subtitle": "Limited time deal",
                            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqhmyBRCngkU_OKSL6gBQxCSH-cufgmZwb2w&usqp=CAU",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Grab Now",
                                    "payload": "/express_offer"
                                }
                            ]
                        },
                        {
                            "title": "Flat ₹100 Off on Next-Day Delivery",
                            "subtitle": "Valid till July 15",
                            "image_url": "https://image.freepik.com/free-vector/city-illustration_23-2147514701.jpg",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Book Now",
                                    "payload": "/next_day_offer"
                                }
                            ]
                        },
                        {
                            "title": "Free Tracking for Premium Users",
                            "subtitle": "Track shipments at no cost",
                            "image_url": "https://img.freepik.com/free-vector/delivery-concept-illustration_114360-5000.jpg",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Know More",
                                    "payload": "/tracking_offer"
                                }
                            ]
                        }
                    ]
                }
            }

        dispatcher.utter_message(attachment=carousel)
        return []
       
class ActionSubmitAWB(Action):
    def name(self) -> Text:
        return "action_track_shipment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language = tracker.get_slot("language1")
        awb_number = next(tracker.get_latest_entity_values("awb_number"), None)

        if not awb_number:
            awb_number = tracker.latest_message.get("text")

        if language == "hindi":
            message = f"✅ आपका पार्सल एडब्ल्यूबी {awb_number} ट्रांजिट में है और इसके कल शाम तक डिलीवर होने की उम्मीद है।"
        else:
            message = f"✅ Your package with AWB {awb_number} is in transit and expected to be delivered by tomorrow evening."

        dispatcher.utter_message(text=message)
        return [SlotSet("awb_number", None)]


class ActionCheckDelay(Action):
    def name(self) -> Text:
        return "action_check_delay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language = tracker.get_slot("language1")
        awb_number = next(tracker.get_latest_entity_values("awb_number"), None)

        if not awb_number:
            awb_number = tracker.latest_message.get("text")

        if language == "hindi":
            message = f" शिपमेंट एडब्ल्यूबी {awb_number} स्थानीय मौसम के कारण विलंबित है। अब यह कल तक डिलीवर होने की उम्मीद है।"
        else:
            message = f"Shipment {awb_number} is delayed due to local weather. New delivery expected by tomorrow."

        dispatcher.utter_message(text=message)
        return [SlotSet("awb_number", None)]

class ActionSummarizeSentiment(Action):

    def name(self) -> Text:
        return "action_summarize_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.get_slot("language1")
        # dispatcher.utter_message(text=f"Thank you for using our service. We appreciate your feedback. Have a great day! 👋")

        # Gather conversation history
        messages = []
        for e in tracker.events:
            if e.get("event") == "user":
                messages.append(f"User: {e.get('text')}")
            elif e.get("event") == "bot":
                messages.append(f"Bot: {e.get('text')}")

        chat_text = "\n".join(messages)

        # Get sender/user ID and timestamp
        sender_id = tracker.sender_id
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🗂 Define filenames
        full_history_file = "chat_history.txt"
        latest_file = "latest_chat.txt"

        conversation_block = f"\n\n==== Conversation @ {timestamp} | User ID: {sender_id} ====\n{chat_text}"

        try:
            # ✅ Append to full chat history
            with open(full_history_file, "a") as file:
                file.write(conversation_block)

            # ✅ Overwrite latest chat
            with open(latest_file, "w") as file:
                file.write(conversation_block)

            # dispatcher.utter_message(text="📄 Your conversation has been saved and analyzed.")

        except Exception as e:
            dispatcher.utter_message(text=f"❌ Error saving conversation: {str(e)}")
        
        # Step 1: Read the latest chat
        try:
            with open(latest_file, "r") as f:
                content = f.read()
        except Exception as e:
            dispatcher.utter_message(text=f"❌ Failed to read latest chat: {str(e)}")
            return []

        # Step 2: Extract rating (default if not found)
        rating = "N/A"
        for line in content.splitlines():
            if "/rate_experience" in line:
                try:
                    rating_json = json.loads(line.split("/rate_experience")[-1])
                    rating = rating_json.get("rating_value", "N/A")
                    break
                except Exception as e:
                    rating = "N/A"    
        
       # Step 3: Send to Ollama LLaMA 3.2 model
        prompt = f"""You are a helpful assistant. Analyze the chatbot conversation below which will be either in English or Hindi language and respond with:

1. A **short summary** (max 2-3 lines).
2. The **overall sentiment**: Positive, Negative, or Neutral.
3. A **sentiment score** between -1 (very negative) and +1 (very positive).
4. The **language** used in the conversation.


Conversation:
{content}

User Rating: {rating}

Language used: {language}

Respond strictly in the following format:
Summary: <very short summary>
Sentiment: <Positive/Negative/Neutral>
Score: <sentiment score>
Language: <language>

"""
        try:
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "llama3.2:latest",
                    "prompt": prompt,
                    "stream": False
                }
            )
            llama_result = response.json().get("response")
        except Exception as e:
            dispatcher.utter_message(text=f"❌ Failed to call LLaMA model: {str(e)}")
            return []
        
        # Step 4: Save result to new file
        summary_filename = f"Summary&Sentiment.txt"
        try:
            with open(summary_filename, "a") as f:
                f.write("\n\n==== Summary Report ====\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"User ID: {sender_id}\n")
                f.write(f"Rating: {rating}\n\n")
                f.write(llama_result)
        except Exception as e:
            dispatcher.utter_message(text=f"❌ Could not save summary file: {str(e)}")
            return []
        
        with open("llama_output.json", "w", encoding="utf-8") as f:
           json.dump({"response": llama_result}, f, ensure_ascii=False, indent=4)
        
        # # Save as a .txt file, formatted as JSON
        # with open("llama_output.txt", "w", encoding="utf-8") as f:
        #    f.write(json.dumps({"response": llama_result}, ensure_ascii=False, indent=4))
        return []




# class ActionDetectLanguage(Action):
#     def name(self) -> Text:
#         return "action_detect_language"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_text = tracker.latest_message.get("text")
#         lang = detect(user_text)
#         return [SlotSet("language", lang)]
    
class ActionAskAwbNo(Action):
    def name(self) -> Text:
        return "action_ask_awb_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        
        
        dispatcher.utter_message(response="utter_ask_awb_no.")

        return []    

class ActionCancelShipment(Action):
    def name(self) -> Text:
        return "action_cancel_shipment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language1")
        # user_text = tracker.latest_message.get("text")
        # # Safely detect language
        # try:
        #     lang = detect(user_text)
        # except LangDetectException:
        #     lang = tracker.get_slot("language")  # fallback to slot 
            
        awb_number = next(tracker.get_latest_entity_values("awb_number"), None)
        if not awb_number:
            awb_number = tracker.latest_message.get("text")

        

        if language == "hindi":
            message = f"शिपमेंट {awb_number} रद्द कर दी गई है।"
        else:
            message = f"Shipment {awb_number} has been cancelled."

        dispatcher.utter_message(text=message)

        return [SlotSet("awb_number", None)]