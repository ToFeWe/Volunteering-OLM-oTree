from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
import random
import datetime
import math
import itertools
import random
import numpy as np

author = 'Tobias Felix Werner'

doc = """
Your app description
"""


def seconds_to_minutes(seconds, rounds):
    total_seconds = seconds * rounds
    minutes = total_seconds / 60
    return round(minutes, 2)


def total_seconds_to_minutes(total_seconds):
    minutes = total_seconds / 60
    minutes_rounded = round(minutes, 2)
    return minutes_rounded


class Constants(BaseConstants):
    name_in_url = 'vod_field'
    players_per_group = None

    # Number of rounds before and after volunteering
    # Note that I cannot put this in the config as we need to define *num_rounds*
    # here but we cannot reference *self.session.config*.
    num_rounds_before = 30
    num_rounds_after = 30
    vod_round = num_rounds_before
    num_rounds = num_rounds_after + num_rounds_before

    # Group size dict
    group_dict = {
        'small_group': {
            'mean': 3,
            'spread': 1,
            'threshold_unc': 400,
            'threshold_cert': 400
        },
        'medium_group': {
            'mean': 30,
            'spread': 10,
            'threshold_unc': 400,
            'threshold_cert': 400
        },
        'big_group': {
            'mean': 300,
            'spread': 100,
            'threshold_unc': 400,
            'threshold_cert': 400
        }
    }

    # Time variables in seconds
    lb_time_per_round = 15
    ub_time_per_round = 30

    # Time variables as displayed
    lb_minutes = seconds_to_minutes(lb_time_per_round, num_rounds_before)
    ub_minutes = seconds_to_minutes(ub_time_per_round, num_rounds_before)

    # Comments to be rated
    with open('./vod_field/static/comments/long_comments.csv', encoding="utf8") as comment_file:
        # TODO: Clean csv beforehand from , ; etc that is in the sentences
        comments = list(csv.DictReader(comment_file, delimiter='\t'))


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        print(self.session.vars)
        return {'vars': self.session.vars}

    def creating_session(self):
        # Assign the comments to be rated.
        print('I am still alive ', self.round_number)
        for p in self.get_players():
            if self.round_number == 1:
                randomized_comments = random.sample(
                    Constants.comments, Constants.num_rounds)
                p.participant.vars['comments'] = randomized_comments

                # save round numbers in session dict as we have to use it in
                # another app
                self.session.vars['num_rounds_before'] = Constants.num_rounds_before
                self.session.vars['num_rounds_after'] = Constants.num_rounds_after

                # Create counter variables in the session dict
                for key in Constants.group_dict.keys():
                    self.session.vars[key] = {}
                    self.session.vars[key]['finished_unc'] = 0
                    self.session.vars[key]['finished_cert'] = 0

                # variable which indicates if the new player gets rejected
                self.session.vars['admit'] = True

            # assign the values for each round
            comment_data = p.current_question()
            p.order_id = int(comment_data['order_id'])
            p.comment = comment_data['comment']
            p.img_id = int(comment_data['img_id'])
            p.comment_subject_id = int(comment_data['ID'])

            # We have to change the displayed round number and the number
            # of total comments given if he volunteered or if it is before
            # the volunteering decision.
            if p.round_number > Constants.vod_round:
                p.ceiling_rounds = Constants.num_rounds_after
                p.displayed_rounds = p.round_number - Constants.num_rounds_before
            else:
                p.ceiling_rounds = Constants.num_rounds_before
                p.displayed_rounds = p.round_number


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    order_id = models.IntegerField()
    comment = models.StringField()
    img_id = models.IntegerField()
    comment_subject_id = models.IntegerField()

    q1 = models.StringField(
        initial=None,
        choices=[('1', 'sehr freundlich'),
                 ('2', '2'),
                 ('3', '3'),
                 ('4', '4'),
                 ('5', '5'),
                 ('6', '6'),
                 ('7', '7'),
                 ('8', '8'),
                 ('9', 'sehr feindselig'),
                 ('Nicht zu bewerten', 'Nicht zu bewerten')],
        verbose_name='Ist der Kommentar freundlich oder feindselig gegenüber der im Foto dargestellten Gruppe? ',
        widget=widgets.RadioSelectHorizontal())

    against_other = models.StringField(
        initial=None,
        choices=[
            'Nein',
            'Ja, er ist zustimmend',
            'Ja, er ist ablehnend',
            'Nicht zu bewerten'],
        verbose_name='Richtet sich der Kommentar an einen anderen Nutzer?',
        widget=widgets.RadioSelectHorizontal())
    should_allow = models.StringField(
        initial=None, choices=['Nein', 'Ja', 'Ich weiß nicht'],
        verbose_name='Sollte dieser Kommentar in einem Internetforum erlaubt sein?',
        widget=widgets.RadioSelectHorizontal())

    c_1 = models.CharField(widget=widgets.CheckboxInput(
    ), blank=True, verbose_name='Beinhaltet negative Vorurteile')
    c_2 = models.CharField(widget=widgets.CheckboxInput(
    ), blank=True, verbose_name='Nutzt rassistische Beleidigungen')
    c_3 = models.CharField(
        widget=widgets.CheckboxInput(),
        blank=True,
        verbose_name='Beinhaltet  beleidigende, erniedrigende oder abwertende Worte')
    c_4 = models.CharField(
        widget=widgets.CheckboxInput(),
        blank=True,
        verbose_name='Ruft zu Gewalt, Drohungen oder Diskriminierung auf')
    c_5 = models.CharField(widget=widgets.CheckboxInput(
    ), blank=True, verbose_name='Nutzt sexistische Beleidigungen')
    c_6 = models.CharField(
        widget=widgets.CheckboxInput(),
        blank=True,
        verbose_name='Die sexuelle Orientierung oder das Geschlecht/Gender wird  herabgesetzt oder stigmatisiert')

    # For the layout
    ceiling_rounds = models.IntegerField()
    displayed_rounds = models.IntegerField()

    # Control variable
    current_time = models.DateTimeField()

    # treatments
    pop_uncertain = models.BooleanField()
    group_size = models.StringField()

    # If we the person was admitted to the treatments or blocked because we
    # are full
    admit = models.BooleanField()

    # Outcome variable
    volunteer_decision = models.BooleanField()

    def current_question(self):
        return self.participant.vars['comments'][self.round_number - 1]

    def get_time_diff(self):
        time_end = self.in_round(Constants.vod_round).current_time
        start_time = self.participant.vars['time_start']

        time_task = time_end - start_time
        return time_task

    def is_playing(self):
        pass

    def get_additional_constants(self):
        """ A function which returns constants stored in the config for the template"""

        group_key = self.participant.vars['group_size']
        pop_unc = self.participant.vars['pop_uncertain']

        spread = Constants.group_dict[group_key]['spread']
        mean_group_size = Constants.group_dict[group_key]['mean']
        lb_group_size = mean_group_size - spread
        ub_group_size = mean_group_size + spread

        baseline_fee = self.session.config['participation_fee']
        vod_bonus = self.session.config['vod_bonus']
        return {
            'mean_group_size': mean_group_size,
            'ub_group_size': ub_group_size,
            'lb_group_size': lb_group_size,
            'baseline_fee': baseline_fee,
            'vod_bonus': vod_bonus,
            'pop_uncertain': pop_unc
        }

    def assign_treatment(self):
        prob_list, total_missing = self.calc_probs()

        # If there are no spots to fill, set the *admit* variable to false to
        # block the participants
        if total_missing > 0:
            treatments, probs = zip(*prob_list)
            treatments_list = list(treatments)

            # because numpy is weird when drawing from a list of tuples we do
            # it like this:
            random_index = int(np.random.choice(len(treatments), 1, p=probs))
            treatment = treatments[random_index]

            # assign treatment according to random draw
            self.group_size, self.pop_uncertain = treatment

            # Also save in the participant dict
            self.participant.vars['pop_uncertain'] = self.pop_uncertain
            self.participant.vars['group_size'] = self.group_size
            self.admit = True

        else:
            self.session.vars['admit'] = False
            self.admit = False

    def calc_probs(self):
        prob_list = []
        missing_treatments = {}
        total_missing = 0
        for key in Constants.group_dict.keys():
            missing_treatments[key] = {}

            diff_cert = Constants.group_dict[key]['threshold_cert'] - \
                self.session.vars[key]['finished_cert']
            diff_unc = Constants.group_dict[key]['threshold_unc'] - \
                self.session.vars[key]['finished_unc']

            # If players join at the same time a lot it can happen that
            # threshold_cert< finished_cert
            if diff_cert < 0:
                missing_treatments[key]['cert'] = 0
            else:
                missing_treatments[key]['cert'] = diff_cert

            if diff_unc < 0:
                missing_treatments[key]['unc'] = 0
            else:
                missing_treatments[key]['unc'] = diff_unc
            total_missing = missing_treatments[key]['cert'] + \
                missing_treatments[key]['unc'] + total_missing

        for key in Constants.group_dict.keys():
            if total_missing > 0:
                current_prob_cert = missing_treatments[key]['cert'] / \
                    total_missing
                current_prob_unc = missing_treatments[key]['unc'] / \
                    total_missing
                # If players join at the same time a lot it can happen that
                # threshold_cert< finished_cert
                if current_prob_cert < 0:
                    current_prob_cert = 0
                if current_prob_unc < 0:
                    current_prob_cert = 0
            else:
                current_prob_cert = 0
                current_prob_unc = 0

            # Append the probability for population uncertainty for the given
            # group size
            prob_list.append(
                ((key, True), current_prob_unc)
            )

            # The same for non population uncertainty
            prob_list.append(
                ((key, False), current_prob_cert)
            )

        return prob_list, total_missing

    def increase_counter(self):
        key = self.participant.vars['group_size']
        if self.participant.vars['pop_uncertain'] is True:
            self.session.vars[key]['finished_unc'] = self.session.vars[key][
                'finished_unc'] + 1
        if self.participant.vars['pop_uncertain'] is False:
            self.session.vars[key]['finished_cert'] = self.session.vars[key][
                'finished_cert'] + 1
