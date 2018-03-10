from api import Api
API_ENDPOINT = "http://192.168.43.222:6001/api"




    

def main():
    api = Api(API_ENDPOINT)
    print(api.getPlayerInfo()) 
    print(api.sendAction("shoot")) 
    print(api.turn(200))
    print(api.getObjects(1000))
if __name__ == "__main__":
    main()
