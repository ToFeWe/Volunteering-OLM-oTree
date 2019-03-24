from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        assert Constants.exit_code in self.html

        if self.player.participant.vars['volunteer_decision']:
            assert 'Da Sie freiwillig die' in self.html
        else:
            assert 'nicht freiwillig' in self.html
            assert 'sofern sich eine andere Person Ihres Teams freiwillig' in self.html

        yield (pages.Results, {'clickworker_id': 'test_name'})
        assert Constants.exit_code in self.html
