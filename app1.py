from HotelRecommendationBot import HotelRecommendationBot
if __name__=='__main__':
    print("Welcome to Hotel Recommendation chatbot");
    print("===================================================");
    hotelBot = HotelRecommendationBot()
    #hotelBot.dialog_management_system()
    hotelBot.deploy()
    print("===================================================");
    print("Thank you for choosing Hotel Recommendation chatbot");
