import graphene
from .models import Player, Team, Conference, Division, Venue, Statline, Roster

class Query:
    player = graphene.List(Player, id=graphene.ID(), team=graphene.String(), full_name=graphene.String(), 
    first_name=graphene.String(), last_name=graphene.String(), primary_number=graphene.Int(),
    current_age=graphene.Int(), nationality=graphene.String(), on_current_roster=graphene.Boolean())

    team = graphene.List(Team, id=graphene.ID(), abbreviation=graphene.String(), team_name=graphene.String(),
    division=graphene.String(), conference=graphene.String(), active=graphene.Boolean())


    def resolve_player(self, info, team, full_name, first_name, last_name, primary_number, division, on_current_roster, current_age, nationality):
        return Player.objects.all().filter(team=team, full_name=full_name, first_name=first_name, last_name=last_name, primary_number=primary_number, division=division, on_current_roster=on_current_roster, current_age=current_age, nationality=nationality)
        
    def resolve_team(self, info, abbreviation, team_name, division, conference, active):
        return Team.objects.all().filter(abbreviation=abbreviation, team_name=team_name, division=division, conference=conference, active=active)



schema = graphene.Schema(query=Query)
