from RiotAPI import RiotAPI
import RiotConstants as Consts
import json
import time
import threading
import winsound

def main():
    status=input("Press enter to continue, or enter h for help:")
    if status == "h":
        print("Welcome to the League Notifier. You will be prompted for a Summoner Name and a Region")
        print('Valid regions are: north_america, brazil, europe_north, europe_west,japan, korea, latin_america_north, latin_america_south, oceana, turkey,russia, pbe')
    name,region=get_name_region()
    api,summoner_ID=load_api_name(name,region)
    info=get_game_info(api,summoner_ID)
    begin_time=info['gameStartTime']
    start=round(begin_time/1000)
    starttime=time.time()
    try:
        while True:
            printit(start,time.time())
            time.sleep(2 - ((time.time() - starttime) % 2))
            update = update_tracking(api,summoner_ID)
            if("status" in update):
                print('Game over!!')
                break
        winsound.Beep(1000,200000)
    except KeyboardInterrupt:
        pass

def get_name_region():
    name=input("Summoner Name: ")
    name=name.replace(" ", "")
    region=input("Summoner Region: ")
    while region not in Consts.REGIONS:
        print('Valid regions are: north_america, brazil, europe_north, europe_west,japan, korea, latin_america_north, latin_america_south, oceana, turkey,russia, pbe')
        region=input("Please enter a valid region: ")
    return name,region

def load_api_name(name,region):
    api = RiotAPI(API_KEY_HERE,Consts.REGIONS[region])
    name_request= api.get_summoner_by_name(name)
    if("status" in name_request.text):
        print("Summoner not found, re-enter information or quit")
        name,region=get_name_region()
        load_api_name(name,region)
    info=json.loads(name_request.text)
    return api,info["id"]

def get_game_info(api,summoner_ID):
    game_info = api.get_game_info(summoner_ID)
    if("status" in game_info.text):
        print("Summoner not in game, enter another summoner or quit")
        name,region=get_name_region()
        api,summoner_ID=load_api_name(name,region)
        get_game_info(api,summoner_ID)
    info=json.loads(game_info.text)
    return info

def update_tracking(api,summoner_ID):
    game_info = api.get_game_info(summoner_ID)
    info=json.loads(game_info.text)
    return info

def printit(x,y):
  duration=y-x
  print("Game Time: " + time.strftime("%H:%M:%S", time.gmtime(duration)))

if __name__ == "__main__":
    main()
