from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    cases = ['all_volunteer', 'no_volunteer', 'random_volunteers']

    def play_round(self):
        case = self.case
        if case == 'all_volunteer':
            # start game
            if self.player.round_number == 1:
                yield (pages.GroupMatchingPage)

            if self.session.vars['admit']:
                if self.player.round_number == 1:
                    assert (self.player.in_round(1).pop_uncertain is True) or (
                        self.player.in_round(1).pop_uncertain is False)
                    if self.player.in_round(1).pop_uncertain is True:
                        assert 'bis' in self.html
                        lb = Constants.group_dict[self.player.in_round(
                            1).group_size]['mean'] - Constants.group_dict[self.player.in_round(1).group_size]['spread']
                        assert str(lb) in self.html
                    else:
                        assert 'genau' in self.html
                        mean = Constants.group_dict[self.player.in_round(
                            1).group_size]['mean']
                        assert str(mean) in self.html
                    yield (pages.Introduction)

                if (
                    self.player.round_number <= Constants.vod_round) or (
                    self.player.round_number > Constants.vod_round and self.player.in_round(
                        Constants.vod_round).volunteer_decision is True):

                    assert (str(Constants.num_rounds_before) or str(
                        Constants.num_rounds_after))in self.html

                    yield (pages.RateComment, {'q1': '9', 'against_other': 'Ja, er ist zustimmend', 'should_allow': 'Ja'})

                if self.player.round_number == Constants.vod_round:
                    yield (pages.VOD, {'volunteer_decision': True})
                    print(self.session.vars)

            else:
                assert 'Leider sind bereits alle Aufgaben bearbeitet worden' in self.html

        if case == 'no_volunteer':
            # start game
            if self.player.round_number == 1:
                yield (pages.GroupMatchingPage)

            if self.session.vars['admit']:
                if self.player.round_number == 1:
                    assert (self.player.in_round(1).pop_uncertain is True) or (
                        self.player.in_round(1).pop_uncertain is False)
                    if self.player.in_round(1).pop_uncertain is True:
                        assert 'bis' in self.html
                        lb = Constants.group_dict[self.player.in_round(
                            1).group_size]['mean'] - Constants.group_dict[self.player.in_round(1).group_size]['spread']
                        assert str(lb) in self.html
                    else:
                        assert 'genau' in self.html
                        mean = Constants.group_dict[self.player.in_round(
                            1).group_size]['mean']
                        assert str(mean) in self.html
                    yield (pages.Introduction)

                if (
                    self.player.round_number <= Constants.vod_round) or (
                    self.player.round_number > Constants.vod_round and self.player.in_round(
                        Constants.vod_round).volunteer_decision is True):
                    yield (pages.RateComment, {'q1': 'Nicht zu bewerten', 'against_other': 'Nicht zu bewerten', 'should_allow': 'Nein'})

                if self.player.round_number == Constants.vod_round:
                    yield (pages.VOD, {'volunteer_decision': False})
                    print(self.session.vars)

            else:
                assert 'Leider sind bereits alle Aufgaben bearbeitet worden' in self.html

        if case == 'random_volunteers':
            # start game
            if self.player.round_number == 1:
                yield (pages.GroupMatchingPage)

            if self.session.vars['admit']:
                if self.player.round_number == 1:
                    assert (self.player.in_round(1).pop_uncertain is True) or (
                        self.player.in_round(1).pop_uncertain is False)
                    if self.player.in_round(1).pop_uncertain is True:
                        assert 'bis' in self.html
                        lb = Constants.group_dict[self.player.in_round(
                            1).group_size]['mean'] - Constants.group_dict[self.player.in_round(1).group_size]['spread']
                        assert str(lb) in self.html
                    else:
                        assert 'genau' in self.html
                        mean = Constants.group_dict[self.player.in_round(
                            1).group_size]['mean']
                        assert str(mean) in self.html

                    yield (pages.Introduction)

                if (
                    self.player.round_number <= Constants.vod_round) or (
                    self.player.round_number > Constants.vod_round and self.player.in_round(
                        Constants.vod_round).volunteer_decision is True):
                    yield (pages.RateComment, {'q1': '4', 'against_other': 'Nein', 'should_allow': 'Ich weiß nicht'})

                if self.player.round_number == Constants.vod_round:
                    choice = random.choice((True, False))
                    yield (pages.VOD, {'volunteer_decision': choice})
                    print(self.session.vars)

            else:
                assert 'Leider sind bereits alle Aufgaben bearbeitet worden' in self.html
