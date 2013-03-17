import re
from datetime                       import  datetime

from mongoengine                    import  *
from mongoengine.django.auth        import  User


class PhoneField(StringField):          # Validate phone numbers
    """
    A field that validates input as a phone number.
    """

    PHONE_REGEX = re.compile(r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$')

    def validate(self, value):
        if value and value != ' ':
            if not PhoneField.PHONE_REGEX.match(value):
                raise ValidationError('Invalid Phone number: %s' % value)

class League( Document ):
    """
    Defines the league
    """
    name            = StringField( max_length = 255 )
    short_name      = StringField( max_length = 20  )
    head            = ReferenceField( 'User' )
    creator         = ReferenceField( 'User' )
    reps            = ListField ( ReferenceField( 'User' ) )
    sport           = StringField( max_length = 50 )
    logo_url        = StringField( required = False, max_length=255 )
    season_start    = DateTimeField( required = False )
    season_end      = DateTimeField( required = False )
    fee             = StringField( max_length = 20  )
    status          = StringField( max_length = 255 )
    is_tournament   = BooleanField( default = False )
    meta = {
        'indexes': ['name']
    }

    def programs(self):
        return Program.objects.filter(league = self)

    def rules(self):
        return LevelRule.objects.filter(league = self)

    def divisions(self):
        return Division.objects.filter(league = self)

    def __unicode__(self):
        return self.name

class Division( Document ):
    """
    Defines divisions in a league, even if no divisions are required the default is D0
    """
    league          = ReferenceField( 'League' )
    name            = StringField( max_length = 255 )

    def __unicode__(self):
        return self.league.name+':'+self.name

class LevelRule( Document ):
    """
    Defines rules for each level
    """
    league          = ReferenceField( 'League' )
    name            = StringField( max_length = 255 )
    cutoff_dob      = DateTimeField( required = False )
    grade           = IntField( required = False )
    priority        = StringField( max_length = 10, default = 'grade')
    measurement     = ListField( EmbeddedDocumentField ( 'Measure') )

class Measure( EmbeddedDocument ):
    """
    Describes measurement reguirements eg. backweight 115 lineweight 135
    """
    describe        = StringField( max_length = 255 )
    measure         = IntField()

class Program( Document ):
    """
    Describes the overall Team organization Teams are in a division of a league
    """
    league          = ReferenceField( 'League' )
    town            = StringField( max_length = 255 )
    name            = StringField( max_length = 255 )
    website         = URLField( required = False )
    creator         = ReferenceField('User')
    head            = ReferenceField('User')
    admins          = ListField( ReferenceField('User')  )
    coachs          = ListField( ReferenceField('User')  )
    fee             = DecimalField()
    logo_url        = StringField( max_length = 255 )

    meta = {
        'indexes': ['name','town']
    }

    def levels(self):
        return Level.objects.filter(program = self)

    def fields(self):
        return GameField.objects.filter(program = self)

    def players(self):
        return [level.players() for level in self.level.players() ]

    def __unicode__(self):
        return self.town + ' ' +self.name

class Level( Document ):
    """
    Describes each individual team within a specific team eg. Freshman/JV/Varsity
    """
    program         = ReferenceField( 'Program' )
    name            = StringField( max_length = 100 )     # Used for levels such as PW/Jr/Sr 8U/11U Fr/V
    head            = ReferenceField( 'User' )
    coaches         = ListField( ReferenceField( 'User' )  )
    players         = ListField( ReferenceField( 'TeamPlayer' )  )
    rules           = ReferenceField('LevelRule')

    def teams(self):
        return Team.objects.filter( level = self )

    def __unicode__(self):
        return self.program.name + ':' + self.name

class Team( Document ):
    """
    Describes an individual team eg. A team, B team
    """
    level           = ReferenceField( 'Level' )
    name            = StringField( max_length = 100 )     # Used for squad/team such as A,  B-Green B-White, Practice
    head            = ReferenceField( 'User' )
    coaches         = ListField( ReferenceField( 'User' )  )
    players         = ListField( ReferenceField( 'TeamPlayer' ) )

    def __unicode__(self):
        return self.level + ':' + self.name

class GameField( Document ):
    """
    Describes a field location
    """
    program         = ReferenceField( 'Program' )
    name            = StringField( max_length = 100 )
    address         = StringField( max_length = 100 )
    locate          = GeoPointField()
    directions      = StringField()

    meta = {
        'indexes': ['name']
    }

    def __unicode__(self):
        return self.program +':'+ self.name

class GameFieldReservation( Document ):
    """
    Use this field to reserve the field for anything other than games
    """
    gamefield       = ReferenceField('GameField')
    start_time      = DateTimeField()
    end_time        = DateTimeField()
    description     = StringField()

    def __unicode(self):
        return self.gamefield+self.start_time.strftime('%m/%d/%y %I:%M')


class Game( Document ):
    home_team       = ReferenceField('Level')
    home_score      = IntField()
    away_team       = ReferenceField('Level')
    away_score      = IntField()
    level		    = StringField()
    start_time      = DateTimeField()
    end_time        = DateTimeField()
    gamefield       = ReferenceField('GameField')
    referee         = ListField( ReferenceField('Referee') )
    meta = {
        'indexes':['home_team','away_team'],
        'ordering': ['date']
    }

    def __unicode__(self):
        return self.home_team + ' vs ' + self.away_team

class Profile( Document ):
    user            = ReferenceField('User')
    town            = StringField(max_length = 255)
    address         = StringField(max_length = 255)
    phone           = PhoneField(max_length = 45)
    mobile          = PhoneField(max_length = 45)
    mobile_addr     = EmailField(max_length = 255)
    photo_url       = StringField(max_length = 255)
    programs        = ListField( ReferenceField( 'Program' ) )

    is_coach        = BooleanField()
    is_admin        = BooleanField()
    is_player       = BooleanField()
    is_parent       = BooleanField()

    def __unicode__(self):
        return self.user.last_name  + ', ' + self.user.first_name

    def players(self):
        if not self.is_parent:
            return[]
        return Player.objects.filter( parents = self.user )

class Player( Document ):
    """
    Describe a player
    """
    id_number       = SequenceField()
    first_name      = StringField( max_length = 255 )
    last_name       = StringField( max_length = 255 )
    birthday        = DateTimeField()
    grade           = IntField()
    address         = StringField( max_length = 255 )
    birth_cert      = StringField( max_length = 255 )
    photo           = StringField( max_length = 255 )
    school          = StringField( max_length = 255 )
    parents         = ListField ( ReferenceField ('User') )

    def __unicode__(self):
        return self.last_name + '. ' + self.first_name

class TeamPlayer ( Document ):
    """
    Describe a particular player on a team
    """
    player          = ReferenceField( 'Player' )
    number          = IntField()
    weight          = StringField( max_length = 10 )
    height          = StringField( max_length = 10)
    positions       = ListField( StringField( max_length = 45 ) )
    status          = StringField( max_length = 255 )

    def __unicode__(self):
        return self.player.last_name + '. ' + self.player.first_name

class Referree(Profile):
    fee             = StringField()

class Organization( Document ):
    """
    Describe a school, club, or town
    """
    admins          = ListField( ReferenceField('User') )
    name            = StringField( max_length = 255 )
    address         = StringField( max_length = 255 )
    phone           = PhoneField( max_length = 45 )
    url             = URLField()
    logo            = StringField(max_length = 255)

class MobileProviders(Document):
    title           = StringField( max_length=25 )
    domain          = StringField( max_length=50 )
    mms             = BooleanField( default = False )
    meta = {
        'indexes': ['title']
    }

