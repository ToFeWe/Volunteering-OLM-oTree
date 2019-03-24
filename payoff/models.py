from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Tobias Werner'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'payoff'
    players_per_group = None
    num_rounds = 1
    exit_code = 'test'


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        print(self.session.vars)
        return {'vars': self.session.vars}


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    clickworker_id = models.StringField()
