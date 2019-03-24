from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class IntroQuestions(Page):
    form_model = 'player'
    form_fields = [
        'q_age',
        'q_gender',
        'q_country',
        'q_study_level',
        'q_employment',
        'q_inhabitants',
        'q_politics',
        'q_freq_clickworker',
        'q_freq_task']


class FalkQuestions(Page):
    form_model = 'player'
    form_fields = ['q_extra1', 'q_extra2', 'q_falk1', 'q_falk2', 'q_falk3',
                   'q_falk4', 'q_falk5', 'q_efficiency1']


page_sequence = [
    IntroQuestions,
    FalkQuestions
]
