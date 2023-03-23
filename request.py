import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests_cache

from dateutils import get_month

numberOfWeekByMonth = 8
requests_cache.install_cache('request_cache', backend='sqlite', expire_after=10800, stale_if_error=True,
                             always_revalidate=True, stale_while_revalidate=10800)


async def get_current(firstname, lastname):
    result = []

    for i in range(numberOfWeekByMonth):
        # date = moment.date(moment.now().add(i * 7, 'd')).format('MM/DD/YY')

        date = (datetime.now() + timedelta(days=i * 7)).strftime("%Y-%m-%d")
        print(date)
        data = scrap_week(firstname, lastname, date)

        result.append(data)

    return result


# TEST_URL = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i&Tel=mathis.gauthier&date=22/03/23'
def scrap_week(firstname, lastname, queried_date):
    calendar_url_base_url = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'
    calendar_url_to_scrap = f"{calendar_url_base_url}&Tel={firstname}.{lastname}&date={queried_date}"
    # print(calendar_url_to_scrap)
    response = requests.get(calendar_url_to_scrap)
    if response.status_code != 200:
        raise Exception('An error has occurred whilst trying to scrape the agenda')
    if 'Erreur de parametres' in response.text:
        print({'status_code': response.status_code,
               'response': response.text,
               'url': calendar_url_to_scrap
               })
        raise Exception('E_SCRAPPING_PARAMETERS')

    result = {}
    key = 'week'
    result[key] = {}

    # with open("edt.html", "r") as f:
    #     # Pass the file object to BeautifulSoup's constructor
    #     soup = BeautifulSoup(f, "html.parser")

    soup = BeautifulSoup(response.text, 'html.parser')

    days = soup.find_all('div', {'class': 'Jour'})
    # print(days)

    for day, el in enumerate(days):
        theDay = day
        courses = soup.find_all('div', {'class': 'Case'})
        leftCss = int(float(el['style'].split('left:')[1].split(';')[0].replace('%', '')) + 100)
        for course, el in enumerate(courses):
            if (int(float(el['style'].split('left:')[1].split(';')[0].replace('%', ''))) != int(
                    float(leftCss) + 9)) and (
                    int(float(el['style'].split('left:')[1].split(';')[0].replace('%', ''))) != leftCss or not
            soup.select('.TCJour')[
                course]):
                continue

            day = soup.select('.TCJour')[theDay].text.split(' ')
            print(f"day : {day}")
            # date
            dayDate = day[1]
            dayMonth = get_month(day[2])
            weekday = day[0].lower()
            year = queried_date.split('-')[0]
            date = f"{dayDate}/{dayMonth}/{year}"
            print(f"DATE : {date}")
            # time
            start = el.select('.TChdeb')[0].text[:5]
            end = el.select('.TChdeb')[0].text[8:13]

            # other information
            # print(el.select('.TCase')[0].text.strip())
            subject = el.select('.TCase')[0].text.strip()
            # print(subject)
            # print(el.select('.TCProf')[0].prettify().split('</span>')[1].split('<br/>')[0].strip().replace('\n', ''))
            professor = el.select('.TCProf')[0].prettify().split('</span>')[1].split('<br/>')[0]
            # professor = el.select('.TCProf')[0].text.split('<br>')[0].split('</span>')[1]
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

            # teams_links = el.select('.Teams a')
            # for teams_link in teams_links:
            #     print(f"{teams_link.select('img').get('src')} : {teams_link.get('href')}")
            link = ''
            if el.select('.Teams a'):
                link = el.select('.Teams a')[0].get('href')

            data = {'date': date, 'subject': subject, 'start': start, 'end': end, 'professor': professor, 'room': room,
                    'weekday': weekday, 'bts': bts, 'remote': remote, 'link': link, 'presence': presence}

            if weekday in result[key]:
                result[key][weekday].append(data)
            else:
                result[key][weekday] = [data]

    result = regroup_courses(result)
    return result


def regroup_courses(result):
    response = {}
    key = 'week'
    response[key] = {}

    for week, courses in result['week'].items():
        for i in range(len(courses)):
            if i < len(courses) - 1:
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

# def pushCoursesUtil(response, key, course):
#     if course.weekday in response[key]:
#         response[key][course.weekday].append(course)
#     else:
#         response[key][course.weekday] = [course]
#     return response
