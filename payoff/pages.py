from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):
    form_model = 'player'
    form_fields = ['clickworker_id']

    def vars_for_template(self):
        return {
            'baseline_fee': self.session.config['participation_fee'],
            'vod_bonus': self.session.config['vod_bonus'],
            'vod_choice': self.player.participant.vars['volunteer_decision'],
            'comments_before': self.session.vars['num_rounds_before'],
            'comments_after': self.session.vars['num_rounds_after']
        }


class LeavePage(Page):
    pass


page_sequence = [
    Results,
    LeavePage
]
