from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, total_seconds_to_minutes
import datetime


class GroupMatchingPage(Page):
    timeout_seconds = 2

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.player.assign_treatment()


class TreatmentFull(Page):
    def is_displayed(self):
        return self.round_number == 1 and not self.session.vars['admit']


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # Save the time, when the participant actually starts rating the
        # comments
        time_start = datetime.datetime.now(datetime.timezone.utc)
        self.participant.vars['time_start'] = time_start

    def vars_for_template(self):
        context = self.player.get_additional_constants()
        return context


class RateComment(Page):
    form_model = 'player'
    form_fields = ['q1', 'against_other', 'should_allow',
                   'c_1', 'c_2', 'c_3', 'c_4', 'c_5', 'c_6']

    def before_next_page(self):
        # Save the time of the current page.
        self.player.current_time = datetime.datetime.now(datetime.timezone.utc)

    def is_displayed(self):
        rounds_and_vod = (
            (self.round_number <= Constants.vod_round) or (
                self.round_number > Constants.vod_round and self.player.in_round(
                    Constants.vod_round).volunteer_decision))
        return rounds_and_vod

    def vars_for_template(self):
        return{
            'imgPath': 'pictures/{}.jpg'.format(self.player.img_id)
        }


class VOD(Page):
    form_model = 'player'
    form_fields = ['volunteer_decision']

    def is_displayed(self):
        rounds_and_vod = self.round_number == Constants.vod_round
        return rounds_and_vod

    def vars_for_template(self):
        # Calculate the time
        time_task = self.player.get_time_diff()
        time_task_min = total_seconds_to_minutes(time_task.total_seconds())

        # Get the constants from the config
        context = self.player.get_additional_constants()
        if context['pop_uncertain']:
            pop_text = '{} bis {}'.format(
                context['lb_group_size'], context['ub_group_size'])
        else:
            pop_text = 'genau {}'.format(context['mean_group_size'])

        label_vod = ("Wollen Sie sich in Ihrem Team, das aus {} Personen"
                     " besteht, freiwillig"
                     " melden und die {} weiteren Kommentare"
                     " bewerten?").format(pop_text, Constants.num_rounds_after)

        context.update({
            'time_task_min': time_task_min,
            'label_vod': label_vod
        })
        return context

    def before_next_page(self):
        # If the player arrives at this page, we say he finished the treatment
        self.player.increase_counter()

        # Save the choice for another app
        self.player.participant.vars['volunteer_decision'] = self.player.volunteer_decision


page_sequence = [
    GroupMatchingPage,
    TreatmentFull,
    Introduction,
    RateComment,
    VOD
]
