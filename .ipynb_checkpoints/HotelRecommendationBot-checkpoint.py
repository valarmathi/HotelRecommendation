from modules.InitializeConversation import initial_conversation
from modules.ChatCompletions import get_chat_completions
from modules.ChatCompletions import chat_completions_function_call
from modules.IntentConfirmation import intent_confirmation_layer
import modules.HotelRecommendationUtil as hotelUtil
from modules.Dictionarypresent import dictionary_present
from modules.ModerationCheck import moderation_check

#from modules.IntentConfirmation import intent_confirmation_layer
class HotelRecommendationBot:
    def deploy(self):
        return "hello world!!"
        
    def dialog_management_system(self):
        conversation = initial_conversation()

        introduction = get_chat_completions(conversation)
        
        print(introduction + '\n')

        top_3_hotels = None
    
        user_input = ''
    
        while(user_input != "exit"):
            user_input = input("")
            #moderation = moderation_check(user_input)
            moderation='Not Flagged'
            if moderation == 'Flagged':
                print("Sorry, this message has been flagged. Please restart your conversation.")
                break
    
            if top_3_hotels is None:
                conversation.append({"role": "user", "content": user_input})
    
                response_assistant = get_chat_completions(conversation)
                #moderation = moderation_check(response_assistant)
                moderation='Not Flagged'
                if moderation == 'Flagged':
                    print("Sorry, this message has been flagged. Please restart your conversation.")
                    break
    
                print(response_assistant)
                confirmation = intent_confirmation_layer(response_assistant)
    
                print("Intent Confirmation Yes/No:",confirmation.get('result'))
    
                if "No" in confirmation.get('result'):
                    conversation.append({"role": "assistant", "content": str(response_assistant)})
                    #print("\n" + str(response_assistant) + "\n")
    
                else:
                    #print("\n" + str(response_assistant) + "\n")
                    print('\n' + "Variables extracted!" + '\n')

                    conversation_reco = self.validateUserProfileAndFetchHotels(response_assistant)
            else:
                conversation_reco.append({"role": "user", "content": user_input})
    
                response_asst_reco = get_chat_completions(conversation_reco)
    
                #moderation = moderation_check(response_asst_reco)
                moderation='Not Flagged'
                if moderation == 'Flagged':
                    print("Sorry, this message has been flagged. Please restart your conversation.")
                    break
    
                print('\n' + response_asst_reco + '\n')
                conversation.append({"role": "assistant", "content": response_asst_reco})


    def validateUserProfileAndFetchHotels(self, response_assistant):
        #hotelUtil.updateHotelsCSV()
        #response_assistant = "{'City': 'Banashankari', 'RestaurantType': 'Casual Dining', 'ApproximateCost': 800, 'Cuisine': 'Chinese', 'Votes': 'medium'}"
        response = dictionary_present(response_assistant)
        print(response_assistant,'--- ',response,' ----');
        print("Thank you for providing all the information. Kindly wait, while I fetch the hotel information for you: \n")
        #response = "{ 'City': 'Banashankari', 'RestaurantType': 'Casual Dining', 'ApproximateCost': 8000, 'Cuisine': 'Chinese', 'Votes': 'medium' }"
        top_3_hotels = hotelUtil.compare_hotels_with_user(response)
        #print("top 3 hotels are", top_3_hotels)

        validated_reco = hotelUtil.recommendation_validation(top_3_hotels)
        conversation_reco = hotelUtil.initialize_conv_reco(validated_reco)
        recommendation = get_chat_completions(conversation_reco)

        print(recommendation)
        #moderation = moderation_check(recommendation)
        moderation = 'Not Flagged'
        if moderation == 'Flagged':
            print("Sorry, this message has been flagged. Please restart your conversation.")
            #break

        conversation_reco.append({"role": "assistant", "content": str(recommendation)})

        print(str(recommendation) + '\n')
        return conversation_reco