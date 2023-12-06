from datetime import datetime, date
from datetime import timedelta

import pytz
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, vCalAddress, vText
from dateutils import get_month
from cachetools import cached, TTLCache
from requests_toolbelt.threaded import pool
from dotenv import load_dotenv
import os

load_dotenv()

base_url_server = os.environ.get('BASE_URL_SERVER')

numberOfWeekByMonth = 8


async def get_current(firstname, lastname, format):
    result = []
    urls = []
    requests_response = []
    for i in range(numberOfWeekByMonth):
        date = (datetime.now() + timedelta(days=i * 7)).strftime("%Y-%m-%d")
        calendar_url_base_url = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'
        calendar_url_to_scrap = f"{calendar_url_base_url}&Tel={firstname}.{lastname}&date={date}"
        urls.append(calendar_url_to_scrap)

    p = pool.Pool.from_urls(urls)
    p.join_all()

    new_pool = pool.Pool.from_exceptions(p.exceptions())
    new_pool.join_all()

    for response in p.responses():
        requests_response.append(response)

    for response in new_pool.responses():
        requests_response.append(response)

    requests_response.sort(key=lambda x: x.request_kwargs['url'])

    for response in requests_response:
        result.append(parse_html_per_week(response, firstname, lastname))

    if format is None:
        return result

    ical = generate_ical(result)
    return ical.to_ical().decode('utf-8')


async def get_teams_link(firstname, lastname, date_time):
    parsed_date = date_time.split('T')[0].split('-')
    date_cours = date(int(parsed_date[0]), int(parsed_date[1]), int(parsed_date[2])).strftime("%Y-%m-%d")

    calendar_url_base_url = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'
    calendar_url_to_scrap = f"{calendar_url_base_url}&Tel={firstname}.{lastname}&date={date_cours}"

    response = requests.get(calendar_url_to_scrap)

    if response.status_code != 200:
        raise Exception('An error has occurred whilst trying to scrape the agenda')
    if 'Erreur de parametres' in response.text:
        print({'status_code': response.status_code,
               'response': response.text,
               'url': calendar_url_to_scrap
               })
        raise Exception('E_SCRAPPING_PARAMETERS')

    result = scrap_teams_link(response, date_time)
    return result


@cached(cache=TTLCache(maxsize=1024, ttl=10800))
def parse_html_per_week(week_data, firstname, lastname):
    result = {}
    key = 'week'
    result[key] = {}

    soup = BeautifulSoup(week_data.text, 'html.parser')

    days = soup.find_all('div', {'class': 'Jour'})

    for day, el1 in enumerate(days):
        theDay = day
        courses = soup.find_all('div', {'class': 'Case'})
        leftCss = int(float(el1['style'].split('left:')[1].split(';')[0].replace('%', '')) + 100)
        for course, el in enumerate(courses):
            if (int(float(el['style'].split('left:')[1].split(';')[0].replace('%', ''))) != int(
                    float(leftCss) + 9)) and (
                    int(float(el['style'].split('left:')[1].split(';')[0].replace('%', ''))) != leftCss or not
            soup.select('.TCJour')[course]):
                continue

            day = soup.select('.TCJour')[theDay].text.split(' ')
            # date
            day_date = day[1]
            day_month = get_month(day[2])
            weekday = day[0].lower()
            year = week_data.request_kwargs['url'].split('date=')[1].split('-')[0]
            new_date = (datetime(int(year), int(day_month), int(day_date)) + timedelta(days=7)).strftime("%d/%m/%Y")
            # time
            start = el.select('.TChdeb')[0].text[:5]
            end = el.select('.TChdeb')[0].text[8:13]

            professor = el.select('.TCProf')[0].prettify().split('</span>')[1].split('<br/>')[0]

            subject = el.select('.TCase')[0].text.strip()
            if professor.strip() != '':
                subject = subject.split(professor.strip())[0].strip()
            else:
                professor = 'N/A'
                subject = subject.split('INGENIERIE')[0].strip()

            bts = 'BTS' in professor
            professor = professor.replace('BTS', '').strip()
            room = el.select('.TCSalle')[0].text.replace('Salle:', '').strip()
            remote = 'distanciel' in subject.lower() or 'distanciel' in room.lower()

            # presence
            presence = el.select('.Presence img')
            if presence and presence[0]['src'] == '/img/valide.png' or not presence:
                presence = True
            else:
                presence = False

            formated_date = (datetime(int(year), int(day_month), int(day_date)) + timedelta(days=7)).strftime(
                "%Y-%m-%d")
            link = f"{base_url_server}/v1/teams?firstname={firstname}&lastname={lastname}&date_time={formated_date}T{start}"

            data = {'date': new_date, 'subject': subject, 'start': start, 'end': end, 'professor': professor,
                    'room': room,
                    'weekday': weekday, 'bts': bts, 'remote': remote, 'link': link, 'presence': presence}

            if weekday in result[key]:
                result[key][weekday].append(data)
            else:
                result[key][weekday] = [data]

    result = regroup_courses(result)
    return result


def scrap_teams_link(data, date_time) -> str:
    soup = BeautifulSoup(data.text, 'html.parser')
    days = soup.find_all('div', {'class': 'Jour'})

    parsed_date = date_time.split('T')[0].split('-')
    parsed_time = date_time.split('T')[1]
    date_cours = date(int(parsed_date[0]), int(parsed_date[1]), int(parsed_date[2])).strftime("%d/%m/%Y")

    result_link = ''

    for day, el1 in enumerate(days):
        theDay = day
        courses = soup.find_all('div', {'class': 'Case'})
        leftCss = int(float(el1['style'].split('left:')[1].split(';')[0].replace('%', '')) + 100)
        for course, el in enumerate(courses):
            if (int(float(el['style'].split('left:')[1].split(';')[0].replace('%', ''))) != int(
                    float(leftCss) + 9)) and (
                    int(float(el['style'].split('left:')[1].split(';')[0].replace('%', ''))) != leftCss or not
            soup.select('.TCJour')[course]):
                continue

            day = soup.select('.TCJour')[theDay].text.split(' ')
            # date
            day_date = day[1]
            day_month = get_month(day[2])

            year = date_time.split('T')[0].split('-')[0]
            new_date = (datetime(int(year), int(day_month), int(day_date)) + timedelta(days=7)).strftime("%d/%m/%Y")
            # time
            start = el.select('.TChdeb')[0].text[:5]

            if el.select('.Teams a') and new_date == date_cours and start == parsed_time:
                result_link = el.select('.Teams a')[0].get('href')

    return result_link


def regroup_courses(result):
    response = {}
    key = 'week'
    response[key] = {}

    for week, courses in result['week'].items():
        for i in range(len(courses)):
            if i < len(courses) - 1:
                # Pour que 2x 2heures d'un même cours se transforme en un cours de 4h
                if (courses[i]['date'] == courses[i + 1]['date'] and courses[i]['subject'] == courses[i + 1][
                    'subject'] and courses[i]['end'] == courses[i + 1]['start'] and courses[i]['professor'] ==
                        courses[i + 1]['professor'] and courses[i]['room'] == courses[i + 1]['room'] and courses[i][
                            'weekday'] == courses[i + 1]['weekday'] and courses[i]['bts'] == courses[i + 1]['bts']):
                    course = courses[i]
                    course['end'] = courses[i + 1]['end']
                    response = push_courses_util(response, key, course)
                    i += 1
                else:
                    response = push_courses_util(response, key, courses[i])
            else:
                response = push_courses_util(response, key, courses[i])
    return response


def push_courses_util(response, key, course):
    if course['weekday'] in response[key]:
        response[key][course['weekday']].append(course)
    else:
        response[key][course['weekday']] = [course]
    return response


def generate_ical(result) -> Calendar:
    # init the calendar
    cal = Calendar()
    date_export = datetime.now(tz=pytz.timezone('Europe/Paris')).strftime("%d/%m/%Y %H:%M")
    # Some properties are required to be compliant
    cal.add('prodid', '-//EPSI ICAL // brev.al//')
    cal.add('version', '2.0')
    for week in result:
        for day in week['week']:
            for course in week['week'][day]:
                # Create an event
                event = Event()
                event.add('name', course['subject'])
                event.add('summary', course['subject'])
                event.add('description',
                          f"Distanciel: {course['remote']} \nSalle: {course['room']} \nCours de: {course['start']} à {course['end']} \nProfesseur: {course['professor']} \n(Importé le: {date_export})")

                start_date = datetime.strptime(course['date'] + ' ' + course['start'], '%d/%m/%Y %H:%M')
                end_date = datetime.strptime(course['date'] + ' ' + course['end'], '%d/%m/%Y %H:%M')

                event.add('dtstart', datetime(start_date.year, start_date.month, start_date.day, start_date.hour,
                                              start_date.minute, 0, 0, tzinfo=pytz.timezone('Europe/Paris')))
                event.add('dtend',
                          datetime(end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, 0, 0,
                                   tzinfo=pytz.timezone('Europe/Paris')))
                event.add('dtstamp', datetime.now())
                event.add('link', course['link'])

                # Add the organizer
                organizer = vCalAddress('MAILTO:' + ".".join(str(course['professor']).split(" ")) + '@epsi.fr')

                # Add parameters of the event
                organizer.params['CN'] = vText(course['professor'])
                organizer.params['ROLE'] = vText('Prof')
                event['organizer'] = organizer
                event['location'] = vText(course['room'])
                # Add the event to the calendar
                cal.add_component(event)
    return cal
