from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail


class PlayerBot(Bot):

    def play_round(self):
        yield SubmissionMustFail(pages.IntroQuestions, {'q_age': '26-35',
                                                        'q_gender': 'Anderes',
                                                        'q_country': 'Ausland',
                                                        'q_study_level': 'Bachelorabschluss',
                                                        'q_inhabitants': '200.000 – 500.000',
                                                        'q_employment': 'Student/Ausbildung',
                                                        'q_politics': '0 Rechts',
                                                        'q_freq_clickworker': 180,
                                                        'q_freq_task': -1}
                                 )
        yield SubmissionMustFail(pages.IntroQuestions, {'q_age': '26-35',
                                                        'q_gender': 'Anderes',
                                                        'q_country': 'Ausland',
                                                        'q_study_level': 'Bachelorabschluss',
                                                        'q_inhabitants': '200.000 – 500.000',
                                                        'q_employment': 'Student/Ausbildung',
                                                        'q_politics': '0 Links',
                                                        'q_freq_clickworker': -1,
                                                        'q_freq_task': 100}
                                 )
        yield (pages.IntroQuestions, {'q_age': '26-35',
                                      'q_gender': 'Anderes',
                                      'q_country': 'Ausland',
                                      'q_study_level': 'Bachelorabschluss',
                                      'q_inhabitants': '200.000 – 500.000',
                                      'q_employment': 'Student/Ausbildung',
                                      'q_politics': '0 Links',
                                      'q_freq_clickworker': 130,
                                      'q_freq_task': 200}
               )
        yield SubmissionMustFail(pages.FalkQuestions, {'q_falk1': '2',
                                                       'q_falk2': '3',
                                                       'q_falk3': '4',
                                                       'q_falk4': '5',
                                                       'q_falk5': 1200,
                                                       'q_efficiency1': '1'}
                                 )
        yield SubmissionMustFail(pages.FalkQuestions, {'q_falk1': '2',
                                                       'q_falk2': '3',
                                                       'q_falk3': '4',
                                                       'q_falk4': '5',
                                                       'q_falk5': 100,
                                                       'q_efficiency1': '1'}
                                 )
        yield SubmissionMustFail(pages.FalkQuestions, {'q_falk1': '2',
                                                       'q_falk2': '3',
                                                       'q_falk3': '4',
                                                       'q_falk4': '5',
                                                       'q_falk5': 100,
                                                       'q_extra1': '0',
                                                       'q_extra2': '5'}
                                 )
        yield SubmissionMustFail(pages.FalkQuestions, {'q_falk1': '2',
                                                       'q_falk2': '3',
                                                       'q_falk3': '4',
                                                       'q_falk4': '5',
                                                       'q_falk5': 100,
                                                       'q_extra1': '0',
                                                       'q_extra2': '5',
                                                       'q_efficiency1': '111'}
                                 )

        yield (pages.FalkQuestions, {'q_falk1': '2',
                                     'q_falk2': '3',
                                     'q_falk3': '4',
                                     'q_falk4': '5',
                                     'q_falk5': 100,
                                     'q_extra1': '0',
                                     'q_extra2': '5',
                                     'q_efficiency1': '0'}
               )
