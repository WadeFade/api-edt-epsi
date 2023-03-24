# -- coding: utf-8 --
import unittest
from unittest.mock import MagicMock, patch

from request import scrap_week, regroup_courses, generate_ical


class TestScrapWeek(unittest.TestCase):
    @patch('request.requests.get')
    def test_scrap_week(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200

        with open('test_assets/epsi_response.html', 'r') as f:
            mock_response.text = f.read()
        mock_get.return_value = mock_response
        result = scrap_week('firstname', 'lastname', '2023-03-24')
        self.assertIsInstance(result, dict)


class TestRegroupCourses(unittest.TestCase):
    def test_regroup_courses(self):
        input_data = {'week': {
            'lundi': [{'date': '13/03/2023', 'subject': 'ATELIER COMPOSANT IA', 'start': '08:00', 'end': '12:00',
                       'professor': 'irolla paul', 'room': 'N104(HEP Nantes)', 'weekday': 'lundi', 'bts': False,
                       'remote': False,
                       'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/20/2023&StartMeetingTeams=1875110&StartMeetingTeamsHash=BEF1FF8812356280DDCF016B146C8E2FAAAB81920CD7E07B10D2A8B928BE56D6CC69139B21E700244A277A5D26BA52B870F771325340C27B006BDB62327C5A10&Tel=breval.lefloch',
                       'presence': True},
                      {'date': '13/03/2023', 'subject': 'MODÉLISATION STATIST', 'start': '13:00', 'end': '17:00',
                       'professor': 'mfondoum jean valéry', 'room': 'N104(HEP Nantes)', 'weekday': 'lundi',
                       'bts': False, 'remote': False, 'link': '', 'presence': True}], 'mardi': [
                {'date': '14/03/2023', 'subject': 'ATELIER BIG DATA IA', 'start': '08:00', 'end': '12:00',
                 'professor': 'houbart jean-claude', 'room': 'N221(HEP Nantes)', 'weekday': 'mardi', 'bts': False,
                 'remote': False,
                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/21/2023&StartMeetingTeams=1879180&StartMeetingTeamsHash=E85F534CDB7E57B517239076391CDC75CDEF685E3D0915B9C12CF959AEB900FF8A5E60D46983B57B4EF4BD7C8E86BAB1CFAB403DD4F2B43A7A32CE8911A91B46&Tel=breval.lefloch',
                 'presence': True},
                {'date': '14/03/2023', 'subject': 'MACHINE LEARNING', 'start': '13:00', 'end': '17:00',
                 'professor': 'houbart jean-claude', 'room': 'N213(HEP Nantes)', 'weekday': 'mardi',
                 'bts': False, 'remote': False,
                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/21/2023&StartMeetingTeams=1880922&StartMeetingTeamsHash=32D5B696DEEBA744653B0A5E79A5BB09912DBD809F41AFB735A63D6475EFD1A858A32BA6FF71FE0F1B6BC4DE91E479C78E4A33287A7D10648CC4B52517BA5A39&Tel=breval.lefloch',
                 'presence': True}], 'mercredi': [
                {'date': '15/03/2023', 'subject': 'DATAVISUALISATION', 'start': '08:00', 'end': '12:00',
                 'professor': 'roussel jean-françois', 'room': 'SALLE_14(DISTANCIEL)', 'weekday': 'mercredi',
                 'bts': False,
                 'remote': True,
                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/22/2023&StartMeetingTeams=1883406&StartMeetingTeamsHash=9B5D490FE63C1423C3E1276506B632CFF0B1DBB0528B7955135F3F6313920EFAB9ED08D532D368813205BC50EE7051225765BE72BAC214C5F19CABCF1332EFDC&Tel=breval.lefloch',
                 'presence': True},
                {'date': '15/03/2023', 'subject': 'DATAVISUALISATION', 'start': '13:00', 'end': '17:00',
                 'professor': 'roussel jean-françois', 'room': 'SALLE_14(DISTANCIEL)',
                 'weekday': 'mercredi', 'bts': False, 'remote': True,
                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/22/2023&StartMeetingTeams=1884966&StartMeetingTeamsHash=09D4968F5D339D29DD93A7162E09313AB830A046EB1A3B097366C76A3F3FC2B5B7F49F4C0BE800ECB189BCFC422CF940EC6AB7AAFDA4F08E4CE007774FB6BB25&Tel=breval.lefloch',
                 'presence': True}], 'jeudi': [
                {'date': '16/03/2023', 'subject': 'MACHINE LEARNING', 'start': '08:00', 'end': '12:00',
                 'professor': 'houbart jean-claude', 'room': 'SALLE_13(DISTANCIEL)', 'weekday': 'jeudi', 'bts': False,
                 'remote': True,
                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/23/2023&StartMeetingTeams=1886428&StartMeetingTeamsHash=6B0133E4CEB0FB829F2F742EC138FF7358817B032204DEEF58FA61F19DFDA87FA163308FF6AF9122AC04D84CD8783C6577B2F3DCC3BEBD20C7A59516D9F0C771&Tel=breval.lefloch',
                 'presence': True},
                {'date': '16/03/2023', 'subject': 'ATELIER DEEP LEARNIN', 'start': '13:00', 'end': '17:00',
                 'professor': 'houbart jean-claude', 'room': 'SALLE_13(DISTANCIEL)', 'weekday': 'jeudi', 'bts': False,
                 'remote': True,
                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/23/2023&StartMeetingTeams=1888283&StartMeetingTeamsHash=B4DD2E45B75A78AFDCD54D5EB58360924D77CB429483C67FD489ACDC245660EE237EBF2C597CCAE9BE677F3F00F508A6C5EF2D8E600B3E3E0291C83470394478&Tel=breval.lefloch',
                 'presence': True},
                {'date': '16/03/2023', 'subject': 'CONSEIL DE CLASSE', 'start': '17:00', 'end': '19:00',
                 'professor': 'adde audrey', 'room': 'M: N303, SALLE_13', 'weekday': 'jeudi',
                 'bts': False, 'remote': False,
                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/24/2023&StartMeetingTeams=1889939&StartMeetingTeamsHash=EFCE2C481490CFD1F1FD0F3DBCCD0D1FEEDDE6BD0C1FF5EAD31D791BCFE302E056F5E429D9613149E8B32FC494662F86CEDB46DD1A9A096F604DDC75E1F56CFC&Tel=breval.lefloch',
                 'presence': False}], 'vendredi': [
                {'date': '17/03/2023', 'subject': 'PRESENTATION DOSSIER', 'start': '09:00', 'end': '10:00',
                 'professor': 'adde audrey', 'room': 'N213(HEP Nantes)', 'weekday': 'vendredi', 'bts': False,
                 'remote': False, 'link': '', 'presence': True},
                {'date': '17/03/2023', 'subject': 'CONFERENCE ENTREPRIS', 'start': '10:00', 'end': '12:00',
                 'professor': 'berthelot cassandra', 'room': 'N213(HEP Nantes)', 'weekday': 'vendredi', 'bts': False,
                 'remote': False, 'link': '', 'presence': True},
                {'date': '17/03/2023', 'subject': 'MODELISATION STATIST', 'start': '13:00', 'end': '17:00',
                 'professor': 'mfondoum jean valéry', 'room': 'N213(HEP Nantes)', 'weekday': 'vendredi', 'bts': False,
                 'remote': False, 'link': '', 'presence': True}]}}

        expected_output = {'week': {'lundi': [
            {'date': '13/03/2023', 'subject': 'ATELIER COMPOSANT IA', 'start': '08:00', 'end': '12:00',
             'professor': 'irolla paul', 'room': 'N104(HEP Nantes)', 'weekday': 'lundi', 'bts': False, 'remote': False,
             'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/20/2023&StartMeetingTeams=1875110&StartMeetingTeamsHash=BEF1FF8812356280DDCF016B146C8E2FAAAB81920CD7E07B10D2A8B928BE56D6CC69139B21E700244A277A5D26BA52B870F771325340C27B006BDB62327C5A10&Tel=breval.lefloch',
             'presence': True},
            {'date': '13/03/2023', 'subject': 'MODÉLISATION STATIST', 'start': '13:00', 'end': '17:00',
             'professor': 'mfondoum jean valéry', 'room': 'N104(HEP Nantes)', 'weekday': 'lundi', 'bts': False,
             'remote': False, 'link': '', 'presence': True}], 'mardi': [
            {'date': '14/03/2023', 'subject': 'ATELIER BIG DATA IA', 'start': '08:00', 'end': '12:00',
             'professor': 'houbart jean-claude', 'room': 'N221(HEP Nantes)', 'weekday': 'mardi', 'bts': False,
             'remote': False,
             'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/21/2023&StartMeetingTeams=1879180&StartMeetingTeamsHash=E85F534CDB7E57B517239076391CDC75CDEF685E3D0915B9C12CF959AEB900FF8A5E60D46983B57B4EF4BD7C8E86BAB1CFAB403DD4F2B43A7A32CE8911A91B46&Tel=breval.lefloch',
             'presence': True}, {'date': '14/03/2023', 'subject': 'MACHINE LEARNING', 'start': '13:00', 'end': '17:00',
                                 'professor': 'houbart jean-claude', 'room': 'N213(HEP Nantes)', 'weekday': 'mardi',
                                 'bts': False, 'remote': False,
                                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/21/2023&StartMeetingTeams=1880922&StartMeetingTeamsHash=32D5B696DEEBA744653B0A5E79A5BB09912DBD809F41AFB735A63D6475EFD1A858A32BA6FF71FE0F1B6BC4DE91E479C78E4A33287A7D10648CC4B52517BA5A39&Tel=breval.lefloch',
                                 'presence': True}], 'mercredi': [
            {'date': '15/03/2023', 'subject': 'DATAVISUALISATION', 'start': '08:00', 'end': '12:00',
             'professor': 'roussel jean-françois', 'room': 'SALLE_14(DISTANCIEL)', 'weekday': 'mercredi', 'bts': False,
             'remote': True,
             'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/22/2023&StartMeetingTeams=1883406&StartMeetingTeamsHash=9B5D490FE63C1423C3E1276506B632CFF0B1DBB0528B7955135F3F6313920EFAB9ED08D532D368813205BC50EE7051225765BE72BAC214C5F19CABCF1332EFDC&Tel=breval.lefloch',
             'presence': True}, {'date': '15/03/2023', 'subject': 'DATAVISUALISATION', 'start': '13:00', 'end': '17:00',
                                 'professor': 'roussel jean-françois', 'room': 'SALLE_14(DISTANCIEL)',
                                 'weekday': 'mercredi', 'bts': False, 'remote': True,
                                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/22/2023&StartMeetingTeams=1884966&StartMeetingTeamsHash=09D4968F5D339D29DD93A7162E09313AB830A046EB1A3B097366C76A3F3FC2B5B7F49F4C0BE800ECB189BCFC422CF940EC6AB7AAFDA4F08E4CE007774FB6BB25&Tel=breval.lefloch',
                                 'presence': True}], 'jeudi': [
            {'date': '16/03/2023', 'subject': 'MACHINE LEARNING', 'start': '08:00', 'end': '12:00',
             'professor': 'houbart jean-claude', 'room': 'SALLE_13(DISTANCIEL)', 'weekday': 'jeudi', 'bts': False,
             'remote': True,
             'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/23/2023&StartMeetingTeams=1886428&StartMeetingTeamsHash=6B0133E4CEB0FB829F2F742EC138FF7358817B032204DEEF58FA61F19DFDA87FA163308FF6AF9122AC04D84CD8783C6577B2F3DCC3BEBD20C7A59516D9F0C771&Tel=breval.lefloch',
             'presence': True},
            {'date': '16/03/2023', 'subject': 'ATELIER DEEP LEARNIN', 'start': '13:00', 'end': '17:00',
             'professor': 'houbart jean-claude', 'room': 'SALLE_13(DISTANCIEL)', 'weekday': 'jeudi', 'bts': False,
             'remote': True,
             'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/23/2023&StartMeetingTeams=1888283&StartMeetingTeamsHash=B4DD2E45B75A78AFDCD54D5EB58360924D77CB429483C67FD489ACDC245660EE237EBF2C597CCAE9BE677F3F00F508A6C5EF2D8E600B3E3E0291C83470394478&Tel=breval.lefloch',
             'presence': True}, {'date': '16/03/2023', 'subject': 'CONSEIL DE CLASSE', 'start': '17:00', 'end': '19:00',
                                 'professor': 'adde audrey', 'room': 'M: N303, SALLE_13', 'weekday': 'jeudi',
                                 'bts': False, 'remote': False,
                                 'link': 'https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx?action=posEDTBEECOME&serverID=C&date=03/24/2023&StartMeetingTeams=1889939&StartMeetingTeamsHash=EFCE2C481490CFD1F1FD0F3DBCCD0D1FEEDDE6BD0C1FF5EAD31D791BCFE302E056F5E429D9613149E8B32FC494662F86CEDB46DD1A9A096F604DDC75E1F56CFC&Tel=breval.lefloch',
                                 'presence': False}], 'vendredi': [
            {'date': '17/03/2023', 'subject': 'PRESENTATION DOSSIER', 'start': '09:00', 'end': '10:00',
             'professor': 'adde audrey', 'room': 'N213(HEP Nantes)', 'weekday': 'vendredi', 'bts': False,
             'remote': False, 'link': '', 'presence': True},
            {'date': '17/03/2023', 'subject': 'CONFERENCE ENTREPRIS', 'start': '10:00', 'end': '12:00',
             'professor': 'berthelot cassandra', 'room': 'N213(HEP Nantes)', 'weekday': 'vendredi', 'bts': False,
             'remote': False, 'link': '', 'presence': True},
            {'date': '17/03/2023', 'subject': 'MODELISATION STATIST', 'start': '13:00', 'end': '17:00',
             'professor': 'mfondoum jean valéry', 'room': 'N213(HEP Nantes)', 'weekday': 'vendredi', 'bts': False,
             'remote': False, 'link': '', 'presence': True}]}}
        output = regroup_courses(input_data)
        self.assertEqual(output, expected_output)


class TestGenerateIcal(unittest.TestCase):
    def test_generate_ical(self):
        input_data = [{'week': {'monday': [
            {'date': '24/03/2023', 'subject': 'Maths', 'start': '08:00', 'end': '10:00', 'professor': 'John Doe',
             'room': 'A101', 'weekday': 'monday', 'bts': False, 'remote': False, 'link': '', 'presence': True}]}}]
        expected_output = b'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//EPSI ICAL // brev.al//\r\nBEGIN:VEVENT\r\nSUMMARY:Maths\r\nDTSTART:20230324T080000\r\nDTEND:20230324T100000\r\nDESCRIPTION:Non\\n cours de : 08:00 \xc3\xa0 10:00\\n Professeur : John Doe\\n Lien\r\n  : \r\nLOCATION:A101\r\nNAME:Maths\r\nORGANIZER;NAME="John Doe";ROLE=Prof:MAILTO:John.Doe@epsi.fr\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n'
        output = generate_ical(input_data).to_ical()
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
