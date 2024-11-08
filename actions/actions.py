
'''
This module contains custom actions for a Rasa chatbot. These actions include providing product information, answering FAQs, solving complaints, recommending products, detecting sentiment, handling fallback scenarios, and tracking metrics.
Classes:
    ActionProvideProductInfo: Provides information about a specified product.
    ActionAnswerFAQ: Answers frequently asked questions.
    ActionSolveComplaint: Handles user complaints.
    ActionRecommendProducts: Recommends products based on the user's purchase history.
    ActionDetectSentiment: Analyzes the sentiment of the user's message and adjusts responses accordingly.
    ActionDefaultFallback: Handles unrecognized user inputs by providing a fallback response.
    ActionTrackMetrics: Logs user messages, detected intents, and conversation lengths for performance metrics.
Dependencies:
    - database: Contains functions to get product information, FAQ answers, and product recommendations.
    - typing: Provides type hints for function signatures.
    - rasa_sdk: Provides classes for creating custom actions in Rasa.
    - textblob: Provides sentiment analysis capabilities.
    - logging: Provides logging capabilities for tracking metrics.
'''
from database import get_product_info, get_faq_answer, recommend_products
from typing import Any, Text, Dict, List
from rasa_sdk.events import  SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from textblob import TextBlob
import logging

'''This action will be used to provide information about a specific product.'''
class ActionProvideProductInfo(Action):
    def name(self):
        return "action_provide_product_info"

    def run(self, dispatcher, tracker, domain):
        product_name = tracker.get_slot('product_name')
        product_info = get_product_info(product_name)
        '''Error handling if the product is not found'''
        if product_info:
            dispatcher.utter_message(text=product_info)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any information about that product.")
        return []

'''This action will be used to answer frequently asked questions.'''
class ActionAnswerFAQ(Action):
    def name(self):
        return "action_answer_faq"

    def run(self, dispatcher, tracker, domain):
        question = tracker.get_slot('faq_question')
        answer = get_faq_answer(question)
        dispatcher.utter_message(text=answer)
        return []

'''This action will be used to handle user complaints.'''    
class ActionSolveComplaint(Action):
    def name(self):
        return "action_solve_complaint"

    def run(self, dispatcher, tracker, domain):
        # Logic to handle the complaint
        dispatcher.utter_message(text="We're sorry to hear about your issue. We're looking into it.")
        return []
    
'''This action will be used to recommend products based on the user's purchase history.'''
class ActionRecommendProducts(Action):
    def name(self):
        return "action_recommend_products"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        recommendations = recommend_products(user_id)
        message = f"Based on your purchase history, we recommend: {', '.join(recommendations)}."
        dispatcher.utter_message(text=message)
        return []

'''Using a sentiment analysis library, such as TextBlob, to analyze the user’s message sentiment and adjust responses.'''
class ActionDetectSentiment(Action):
    def name(self):
        return "action_detect_sentiment"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        sentiment = TextBlob(user_message).sentiment.polarity

        if sentiment < -0.3:
            dispatcher.utter_message(text="I sense you're frustrated. Let me help with that.")
        elif sentiment > 0.3:
            dispatcher.utter_message(text="I'm glad to see you're satisfied!")
        else:
            dispatcher.utter_message(text="How can I assist you further?")
        return []

'''This action will add fallback logic to handle unrecognized user inputs.'''
class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I'm not sure how to help with that. Let me connect you with a support agent.")
        return []

'''Each time action_track_metrics is called, the chatbot logs the user’s message, detected intent, and conversation length to chatbot_metrics.log'''
logging.basicConfig(filename='chatbot_metrics.log', level=logging.INFO)

class ActionTrackMetrics(Action):
    def name(self):
        return "action_track_metrics"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        intent = tracker.get_intent_of_latest_message()
        conversation_length = len(tracker.events)

        logging.info(f"User message: {user_message}")
        logging.info(f"Detected intent: {intent}")
        logging.info(f"Conversation length: {conversation_length}")

        dispatcher.utter_message(text="Your message has been logged for performance metrics.")
        return []