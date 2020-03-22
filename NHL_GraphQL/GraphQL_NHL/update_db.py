import requests
from GraphQL_NHL.models import Player, Team, Conference, Division, Statline, Roster
from django.db.models import Q
import operator
from functools import reduce

def update_players_teams_statlines():
    request_result = requests.get("""https://api.nhle.com/stats/rest/skater?isAggregate=false&reportType=basic&isGame=false&reportName=skatersummary&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&cayenneExp=leagueId=133%20and%20gameTypeId=2%20and%20seasonId>=19171918%20and%20seasonId<=20182019""")
    json = request_result.json()
    data = json['data']
    player_ids = []

    for season in data:
        player_ids.append(season["playerId"])

    player_ids = set(player_ids)
    for player_id in player_ids:
        player_info = requests.get("https://statsapi.web.nhl.com/api/v1/people/{}".format(player_id)).json()["people"][0]
        print(player_id)
        if "currentTeam" in player_info.keys():
            Player.objects.create(full_name= player_info["fullName"], first_name=player_info["firstName"], last_name=player_info["lastName"], primary_number=player_info["primaryNumber"],
        team=player_info["currentTeam"]["name"], current_age=player_info["currentAge"], birth_city=player_info["birthCity"], birth_country=player_info["birthCountry"], nationality=player_info["nationality"],
        height=player_info["height"], weight=player_info["weight"], active=player_info["active"], alternate_captain=player_info["alternateCaptain"], captain=player_info["captain"],
        rookie=player_info["rookie"], shoots_catches=player_info["shootsCatches"], on_current_roster=True, birth_date=player_info["birthDate"], nhl_value=player_id, position=player_info["playerPositionCode"])
        else:
            Player.objects.create(full_name= player_info["fullName"], first_name=player_info["firstName"], last_name=player_info["lastName"], primary_number=player_info["primaryNumber"],
            current_age=player_info["currentAge"], birth_city=player_info["birthCity"], birth_country=player_info["birthCountry"], nationality=player_info["nationality"],
            height=player_info["height"], weight=player_info["weight"], active=player_info["active"], alternate_captain=player_info["alternateCaptain"], captain=player_info["captain"],
            rookie=player_info["rookie"], shoots_catches=player_info["shootsCatches"], on_current_roster=True, birth_date=player_info["birthDate"], nhl_value=player_id, position=player_info["playerPositionCode"])

    update_teams()

    aggregate_request_result = requests.get("""https://api.nhle.com/stats/rest/skaters?isAggregate=true&reportType=basic&isGame=false&reportName=skatersummary&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&cayenneExp=leagueId=133%20and%20gameTypeId=2%20and%20seasonId>=19171918%20and%20seasonId<=20182019""")
    aggregate_data = aggregate_request_result.json()["data"]
    for player_statline in aggregate_data:
        player = Player.objects.get(nhl_value=player_statline["playerId"])

        statline = Statline.objects.create(is_aggregate=True, player=player, power_play_goals=player_statline["ppGoals"], power_play_points=player_statline["ppPoints"], shotPercentage=player_statline["shootingPctg"], games=player_statline["gamesPlayed"], years=player_statline["seasonId"], 
        goals=player_statline["goals"], assists=player_statline["assists"], points=player_statline["points"],pim=player_statline["penaltyMinutes"], shots=player_statline["shots"], game_winning_goals=player_statline["gameWinningGoals"], shorthanded_goals=player_statline["shGoals"], shorthanded_points=player_statline["shPoints"])
        player.aggeregate_stats = statline
    
    for season in data:
        player = Player.objects.get(nhl_value=season["playerId"])
        teams=season["playerTeamsPlayedFor"]
        if ',' in teams:
            teams = teams.split(',')

        teams_query=Team.objects.filter(reduce(operator.and_, (Q(abbreviation__contains=x) for x in teams)))
        statline = Statline.objects.create(is_aggregate=False, player=player, team=teams_query, power_play_goals=season["ppGoals"], power_play_points=season["ppPoints"], shotPercentage=season["shootingPctg"], games=season["gamesPlayed"], years=season["seasonId"], goals=season["goals"], assists=season["assists"], points=season["points"],pim=season["penaltyMinutes"], shots=season["shots"], game_winning_goals=season["gameWinningGoals"], shorthanded_goals=season["shGoals"], shorthanded_points=season["shPoints"])

        player.all_stats = statline    
    
def update_teams():
    data = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
    json = data.json()
    data = json["teams"]
    for team in data:
        Team.objects.create(name = team["name"], venue=team["venue"], abbreviation=team["abbreviation"], team_name=team["teamName"], location_name=team["locationName"], first_year_of_play=team["firstYearOfPlay"],
        official_site_url=team["officialSiteUrl"], active=team["active"], nhl_value=team["franchiseId"])
        

def update_divisions():
    data = requests.get("https://statsapi.web.nhl.com/api/v1/divisions")
    json = data.json()
    data = json["divisions"]
    team_data = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
    team_json = team_data.json()
    team_data = team_json["teams"]
    
    for division in data:
        division_obj = Division.objects.create(name=division["name"], nhl_value=division["id"])
        division_team_list = []
        for team in team_data:
            if division["name"] == team["division"]["name"]:
                division_team_list.append(team["id"])
        teams_query=Team.objects.filter(reduce(operator.and_, (Q(abbreviation__contains=x) for x in division_team_list)))
        for team in teams_query:
            team.division= division_obj
        

def update_conferences():
    data = requests.get("https://statsapi.web.nhl.com/api/v1/conferences")
    json = data.json()
    data = json["conferences"]
    team_data = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
    team_json = team_data.json()
    team_data = team_json["teams"]
    
    for conference in data:
        conference_obj = Conference.objects.create(name=conference["name"], nhl_value=conference["id"])
        conference_team_list = []
        for team in team_data:
            if conference["name"] == conference["conference"]["name"]:
                conference_team_list.append(team["id"])
        teams_query=Team.objects.filter(reduce(operator.and_, (Q(abbreviation__contains=x) for x in conference_team_list)))
        for team in teams_query:
            team.conference= conference_obj

def update_rosters():
    current_year=int(((requests.get("https://statsapi.web.nhl.com/api/v1/seasons/current").json())["seasons"][0]["seasonId"])[4:])
    team_ids = []
    team_data = requests.get("https://statsapi.web.nhl.com/api/v1/teams").json()["teams"]
    for team in team_data:
        team_ids.append((team["id"],team["firstYearOfPlay"]))
    for team_id, first_year in team_ids:
        for year in range(int(first_year),current_year):
            roster_info = requests.get("https://statsapi.web.nhl.com/api/v1/teams/{}/?expand=team.roster&season=".format(team_id) + str(year) + str(year + 1)).json()
            roster = roster_info["teams"][0]["roster"]["roster"]
            roster_obj = Roster.objects.create(year=(str(year) + str(year + 1)))
            for player in roster:
                roster_obj.players = Player.objects.get(nhl_value=player["person"]["id"])
            current_team = Team.objects.get(nhl_value=team_id)
            roster_obj.team = current_team
            if year == current_year-1:
                current_team.current_roster = roster_obj
            current_team.all_rosters = roster_obj

def delete_all():
    Team.objects.all().delete()
    Conference.objects.all().delete()
    Player.objects.all().delete()
    Division.objects.all().delete()
    Statline.objects.all().delete()
    Roster.objects.all().delete()



def main(argument):
    delete_all()
    update_players_teams_statlines()
    update_rosters()
    update_divisions()
    update_conferences()
    print("Updated DB!")


if __name__ == '__main__':
    main()
