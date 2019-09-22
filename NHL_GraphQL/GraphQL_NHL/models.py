from django.db import models

class Conference(models.Model):
    name = models.CharField(max_length=100)
    teams = models.ForeignKey(Team, on_delete=models.PROTECT)
    divisions = models.ForeignKey(Division, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Division(models.Model):
    name = models.CharField(max_length=100)
    teams = models.ForeignKey(Team, on_delete=models.PROTECT)
    conference = models.ForeignKey(Conference, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    venue = models.OneToOneField(Venue, on_delete=models.PROTECT,
        primary_key=True)
    abbreviation =  models.CharField(max_length=10)
    team_name = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    first_year_of_play = models.CharField(max_length=10)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    conference = models.ForeignKey(Conference, on_delete=models.PROTECT)
    official_site_url = models.CharField(max_length=100)
    active = models.BooleanField()
    current_roster = models.OneToOneField(Roster, on_delete=models.PROTECT)
    all_rosters = models.ForeignKey(Roster, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Player(models.Model):
    full_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    primary_number = models.IntegerField()
    birth_date = models.DateField()
    current_age = models.IntegerField()
    birth_city = models.CharField(max_length=100)
    birth_country = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    weight = models.IntegerField()
    active = models.BooleanField()
    alternate_captain = models.BooleanField()
    captain = models.BooleanField()
    rookie = models.BooleanField()
    shoots_catches = models.CharField(max_length=5)
    on_current_roster = models.BooleanField()
    current_roster = models.ForeignKey(Roster, on_delete=models.PROTECT)

    LEFT_WING = 'LW'
    RIGHT_WING = 'RW'
    CENTRE = 'C'
    LEFT_DEFENSE = 'LD'
    RIGHT_DEFENSE = 'RD'
    GOALIE = 'G'
    POSITION_CHOICES = [
        (LEFT_WING, 'Left Wing'),
        (RIGHT_WING, 'Right Wing'),
        (CENTRE, 'Centre'),
        (LEFT_DEFENSE,'Left Defense'),
        (RIGHT_DEFENSE, 'Right Defense'),
        (GOALIE, 'Goalie')
    ]
    position = models.CharField(max_length=50, choice=POSITION_CHOICES)

    aggregate_stats = models.OneToOneField(Statline, on_delete=models.PROTECT)
    all_stats = models.ForeignKey(Statline, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Statline(models.Model):
    player = models.ForeignKey(Player, models.PROTECT)
    years = models.CharField(max_length=10)
    team = models.ForeignKey(Team, models.PROTECT)
    goals = models.IntegerField()
    assists = models.IntegerField()
    points = models.IntegerField()
    pim = models.IntegerField()
    shots = models.IntegerField()
    games = models.IntegerField()
    power_play_goals = models.IntegerField()
    power_play_points = models.IntegerField()
    shot_percentage = models.DecimalField()
    game_winning_goals = models.IntegerField()
    shorthanded_goals = models.IntegerField()
    shorthanded_points = models.IntegerField()

    def __str__(self):
        return self.name


class Roster(models.Model):
    year = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    players = models.ForeignKey(Player, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.year + " " + self.team
