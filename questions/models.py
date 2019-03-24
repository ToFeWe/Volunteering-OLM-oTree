from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Tobias Werner'

doc = """
Several control questions for the field experiment.
"""


class Constants(BaseConstants):
    name_in_url = 'questions_vod'
    players_per_group = None
    num_rounds = 1
    states = [
        "Baden-Württemberg",
        "Bayern",
        "Berlin",
        "Brandenburg",
        "Bremen",
        "Hamburg",
        "Hessen",
        "Niedersachsen",
        "Mecklenburg-Vorpommern",
        "Nordrhein-Westfalen",
        "Rheinland-Pfalz",
        "Saarland",
        "Sachsen",
        "Sachsen-Anhalt",
        "Schleswig-Holstein",
        "Thüringen",
        "Ausland",
        'keine Angabe']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Allgemeine Fragen
    q_gender = models.StringField(
        choices=['Männlich', 'Weiblich', 'Anderes',
                 'Ich möchte es lieber nicht sagen'],
        label='Geschlecht',
        widget=widgets.RadioSelectHorizontal)

    q_age = models.StringField(
        choices=['18-25', '26-35', '36-45', '46-55', '55+', 'keine Angabe'],
        label='Alter',
        widget=widgets.RadioSelectHorizontal)

    q_country = models.CharField(choices=Constants.states,
                                 label='In welchem Bundesland leben Sie?')

    q_study_level = models.StringField(
        choices=[
            "Weiterführende Schule nicht beendet",
            "Abitur",
            "Bachelorabschluss",
            "Masterabschluss",
            "Berufliche Qualifikation",
            'keine Angabe'],
        label='Was ist Ihr höchster Bildungsabschluss?')

    q_inhabitants = models.StringField(
        choices=[
            "> 1.500.000",
            "500.000 – 1.500.000",
            "200.000 – 500.000",
            "50.000 – 200.000",
            "< 50.000",
            'keine Angabe'],
        label="Was ist Die Einwohnerzahl Ihres derzeitigen Wohnortes?",
        widget=widgets.RadioSelectHorizontal)

    q_employment = models.StringField(
        choices=[
            "Arbeitnehmer",
            "Selbständig",
            "Arbeitssuchend",
            "Nicht erwerbstätig",
            "Im Ruhestand",
            "Student/Ausbildung",
            "Sonstiges",
            'keine Angabe'],
        label="Was ist Ihr Erwerbsstatus?",
        widget=widgets.RadioSelectHorizontal)
    q_politics = models.StringField(
        choices=[
            "0 Links",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10 Rechts",
            'keine Angabe'],
        label="In der Politik wird manchmal von \"Links\" und \"Rechts\" gesprochen. Wo würden Sie sich auf dieser Skala platzieren, wobei 0 \"Links\" und 10 \"Rechts\" bedeutet?",
        widget=widgets.RadioSelectHorizontal)
    # Optional formfield as we do not have a 'no answer' field
    q_freq_clickworker = models.IntegerField(
        initial=None,
        label="Wie viele Stunden haben Sie in der letzten Woche auf Clickworker oder einer vergleichbaren Plattform gearbeitet?",
        min=0,
        max=168,
        blank=True)
    q_freq_task = models.IntegerField(
        initial=None, min=0,
        label="Wie viele Male haben Sie bereits an eine vergleichbaren Aufgabe gearbeitet?",
        blank=True)

    # Extra Questions Amalia
    q_extra1 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', 'trifft voll zu')],
        verbose_name='Ich bin empört, wenn es jemandem unverdient schlechter geht als anderen.',
        doc="""Ich bin empört, wenn es jemandem unverdient schlechter geht als anderen.""",
        widget=widgets.RadioSelectHorizontal())

    q_extra2 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', 'trifft voll zu')],
        verbose_name='Es macht mir zu schaffen, wenn sich jemand für Dinge abrackern muss, die anderen in den Schoß fallen.',
        doc="""Es macht mir zu schaffen, wenn sich jemand für Dinge abrackern muss, die anderen in den Schoß fallen.""",
        widget=widgets.RadioSelectHorizontal())

    # Efficiency Question
    q_efficiency1 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'trifft voll zu')],
        verbose_name='Ich bin eher bereit Mühen auf mich zu nehmen, wenn viele Leute davon profitieren.',
        doc="""Ich bin eher bereit Mühen auf mich zu nehmen, wenn viele Leute davon profitieren.""",
        widget=widgets.RadioSelectHorizontal())

    # Falk Questions
    q_falk1 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht risikobereit'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr risikobereit')],
        verbose_name='Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?',
        doc="""Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?""",
        widget=widgets.RadioSelectHorizontal())

    q_falk2 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht bereit zu verzichten'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr bereit zu verzichten')],
        verbose_name='Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?',
        doc="""Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?""",
        widget=widgets.RadioSelectHorizontal())

    q_falk3 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'trifft voll zu')],
        verbose_name='Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.',
        doc="""Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.""",
        widget=widgets.RadioSelectHorizontal())

    q_falk4 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht bereit zu bestrafen'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr bereit zu bestrafen')],
        verbose_name='Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?',
        doc="""Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?""",
        widget=widgets.RadioSelectHorizontal())
    q_falk5 = models.IntegerField(
        initial=None, min=0, max=1000,
        verbose_name='Stellen Sie sich folgende Situation vor: Sie haben in einem Preisausschreiben 1.000 € gewonnen. Wie viel würden Sie in Ihrer momentanen Situation für einen gemeinnützigen Zweck spenden?',
        doc="""Stellen Sie sich folgende Situation vor: Sie haben in einem Preisausschreiben 1.000 € gewonnen. Wie viel würden Sie in Ihrer momentanen Situation für einen gemeinnützigen Zweck spenden?""")
