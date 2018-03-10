from api import Api
API_ENDPOINT = "http://192.168.43.222:6666/api"




    

def main():
    api = Api(API_ENDPOINT)
    print(api.getPlayerInfo())  
if __name__ == "__main__":
    main()
