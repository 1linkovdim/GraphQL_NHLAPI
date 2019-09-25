import graphene
from .models import Player, Team, Conference, Division, Venue, Statline, Roster
from graphene_django.types import DjangoObjectType

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player

class TeamType(DjangoObjectType):
    class Meta:
        model = Team

class ConferenceType(DjangoObjectType):
    class Meta:
        model = Conference

class DivisionType(DjangoObjectType):
    class Meta:
        model = Division

class VenueType(DjangoObjectType):
    class Meta:
        model = Venue

class StatlineType(DjangoObjectType):
    class Meta:
        model = Statline

class RosterType(DjangoObjectType):
    class Meta:
        model = Roster

class Query(graphene.ObjectType):
    player = graphene.List(PlayerType, id=graphene.ID(), team=graphene.String(), full_name=graphene.String(), 
    first_name=graphene.String(), last_name=graphene.String(), primary_number=graphene.Int(),
    current_age=graphene.Int(), nationality=graphene.String(), on_current_roster=graphene.Boolean())

    team = graphene.List(TeamType, id=graphene.ID(), abbreviation=graphene.String(), team_name=graphene.String(),
    division=graphene.String(), conference=graphene.String(), active=graphene.Boolean())

    conference = graphene.List(ConferenceType, id=graphene.ID(), name=graphene.String())

    venue = graphene.List(VenueType, id=graphene.ID(), name=graphene.String(), city=graphene.String())
    
    division = graphene.List(DivisionType, id=graphene.ID(), name=graphene.String())

    def resolve_player(self, info, team, full_name, first_name, last_name, primary_number, division, on_current_roster, current_age, nationality):
        return Player.objects.all().filter(team=team, full_name=full_name, first_name=first_name, last_name=last_name, primary_number=primary_number, division=division, on_current_roster=on_current_roster, current_age=current_age, nationality=nationality)
        
    def resolve_team(self, info, abbreviation=None, team_name=None, division=None, conference=None, active=None):
        return Team.objects.all().filter(abbreviation=abbreviation, team_name=team_name, division=division, conference=conference, active=active)

    def resolve_conference(self, info, name=None):
        return Conference.objects.all().filter(name=name)

    def resolve_venue(self, info, name=None, city=None):
        return Venue.objects.all().filter(name=name, city=city)

    def resolve_division(self, info, name=None):
        return Division.objects.all().filter(name=name)

    # def resolve_statline(self, info, player=None, years=None, team=None, goals=None, assists=None, points=None, pim=None, shots=None, games=None, 
    # power_play_goals=None, power_play_points=None, shot_percentage=None, game_winning_goals=None, shorthanded_goals=None, shorthanded_points=None):
    #     return Statline.objects.all().filter(player=player, years=years, team=team, goals=goals, assists=assists, points=points, pim=pim, shots=shots, games=games, power_play_goals=power_play_goals, power_play_points=power_play_points, shot_percentage=shot_percentage, game_winning_goals=game_winning_goals, shorthanded_goals=shorthanded_goals, shorthanded_points=shorthanded_points)

    # def resolve_roster(self, info, year=None, team=None, players=None):
    #     return Roster.objects.all().filter(year=year, team=team, players=players)    

schema = graphene.Schema(query=Query)
