from requests.game_drives import GameDrivesRequestService
from requests.play_by_play import PlayByPlayRequestService
from requests.teams import TeamsRequestService


#  __MAIN__
TeamsRequestService.GetTeamsData()
GameDrivesRequestService.GetGameDrivesData()
PlayByPlayRequestService.GetGameDrivesData()