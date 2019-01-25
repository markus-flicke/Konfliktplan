import argparse

from Mail import Mail
import pandas as pd
from Conflict import Conflict

DEVMODE = False

class Konfliktplan:
    VERANSTALTUNGSLISTE_PATH = 'Veranstaltungen-SoSe19-20190125.csv'
    REGELSTUDIENPLAN_PATH = 'regelstudienplaene_3.csv'

    def __init__(self, term='Sommer', mailto = 'markus.flicke.marburg@gmail.com'):
        self.term = term
        self.mailto = mailto
        self.veranstaltungen, self.regel_studienplan = self._load()

    def run(self):
        conflicts = self._find_conflicts()
        res = self._summarise_conflicts(conflicts)
        self._send(res)

    @staticmethod
    def _summarise_conflicts(conflicts):
        res = []
        for conflict in conflicts:
            title_a = '{} ({} - {})'.format(conflict.data[0].name, str(conflict.data[0].von.strftime('%H:%M')),
                                            str(conflict.data[0].bis.strftime('%H:%M')))
            title_b = '{} ({} - {})'.format(conflict.data[1].name, str(conflict.data[1].von.strftime('%H:%M')),
                                            str(conflict.data[1].bis.strftime('%H:%M')))
            tag = conflict.data[0].Tag
            res.append([conflict.degree, conflict.variant, conflict.semester, tag, title_a, title_b])
        return pd.DataFrame(res, columns=['Studiengang', 'Variante', 'Semester', 'Tag', 'Titel_a', 'Titel_b'])

    def _find_conflicts(self):
        res = []
        for d_name, degree in self.regel_studienplan.groupby('Studiengang'):
            for v_name, variant in degree.groupby('Variante'):
                for s_name, semester in variant.groupby('Semester'):
                    for i in range(len(semester)):
                        for j in range(i + 1, len(semester)):
                            conflicting_events = self._title_conflicts(semester.iloc[i].Titel, semester.iloc[j].Titel)
                            for conflicting_event in conflicting_events:
                                res.append(Conflict(conflicting_event, d_name, v_name, s_name))
        return res

    def _title_conflicts(self, title_a, title_b):
        res = []
        veran_a = self.veranstaltungen.loc[self.veranstaltungen.index == title_a]
        veran_b = self.veranstaltungen.loc[self.veranstaltungen.index == title_b]

        def do_conflict(event_a, event_b):
            if not event_a.Tag == event_b.Tag:
                return False
            s_a = event_a.von
            s_b = event_b.von
            e_a = event_a.bis
            e_b = event_b.bis
            return not (s_a < e_b) ^ (e_a > s_b)

        for i in range(len(veran_a)):
            for j in range(len(veran_b)):
                if do_conflict(veran_a.iloc[i], veran_b.iloc[j]):
                    res.append([veran_a.iloc[i], veran_b.iloc[j]])
        return res

    def _send(self, df):
        body = """<html>
                  <head><style  type="text/css" > th {border: 1px solid black;width: 65px;} td 
                  {border: 1px solid black;} table {border-collapse: collapse;border: 1px solid black;}
                  </style>
                  </head>
                  <body>"""

        body += df.to_html(index=False)
        body += "</body></html>"
        Mail.send(body, subject='Konfliktplan', to=self.mailto)

    def _load(self):
        veranstaltungen = pd.read_csv(self.VERANSTALTUNGSLISTE_PATH)
        veranstaltungen = veranstaltungen.drop('Titel semabh.', axis=1)
        veranstaltungen = veranstaltungen.rename({'Titel semunabh.': 'Titel'}, axis=1)
        veranstaltungen = veranstaltungen.set_index('Titel')
        veranstaltungen.von = pd.to_datetime(veranstaltungen.von, 'coerce', format='%H:%M').apply(pd.datetime.time)
        veranstaltungen.bis = pd.to_datetime(veranstaltungen.bis, 'coerce', format='%H:%M').apply(pd.datetime.time)
        veranstaltungen['Datum von'] = pd.to_datetime(veranstaltungen['Datum von'], 'coerce')
        veranstaltungen['Datum bis'] = pd.to_datetime(veranstaltungen['Datum bis'], 'coerce')
        veranstaltungen = veranstaltungen.loc[veranstaltungen['Rhyth.'] == 'woch']

        regel_studienplan = pd.read_csv(self.REGELSTUDIENPLAN_PATH)
        regel_studienplan = regel_studienplan.loc[regel_studienplan['Anzeigen'].apply(lambda x: x in ('1', '2'))]

        def relevant_subject(row):
            return (row['Variante'] == self.term) ^ (row['Semester'] % 2 == 0)

        regel_studienplan = regel_studienplan.loc[
            regel_studienplan[['Variante', 'Semester']].apply(relevant_subject, axis=1)]
        return veranstaltungen, regel_studienplan


def devmode():
    global DEVMODE
    DEVMODE = True
    print('\nDeveloper mode enabled')
    return True

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mailto', help = 'Email', action = 'store_const')
    return parser.parse_args()


if __name__ == '__main__':
    mailto = 'markus.flicke.marburg@gmail.com'#argparser().mailto
    Konfliktplan(mailto=mailto).run()
