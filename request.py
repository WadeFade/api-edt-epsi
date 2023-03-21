import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

numberOfWeekByMonth = 4


async def get_current(firstname, lastname):
    result = []

    for i in range(numberOfWeekByMonth):
        # date = moment.date(moment.now().add(i * 7, 'd')).format('MM/DD/YY')
        date = (datetime.now() + timedelta(days=i * 7)).strftime("%m/%d/%y")

        data = scrap_week(firstname, lastname, date)

        result.append(data)

    return result


def scrap_week(firstname, lastname, queried_date):
    calendar_url_to_scrap = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'

    response = requests.get(f"{calendar_url_to_scrap}&Tel={firstname}.{lastname}&date={queried_date}")

    if response.status_code != 200:
        raise Exception('An error has occurred whilst trying to scrape the agenda')
    if 'Erreur de parametres' in response.text:
        raise Exception('E_SCRAPPING_PARAMETERS')

    result = {}
    key = 'week'
    result[key] = {}

    soup = BeautifulSoup(response.text, 'html.parser')

    days = soup.find_all('div', {'class': 'Jour'})

    for day, el in enumerate(days):
        theDay = day
        courses = soup.find_all('div', {'class': 'Case'})
        leftCss = int(float(el['style'].split('left: ')[1].split(';')[0]) + 100)

        for course, el in enumerate(courses):
            if (int(float(el['style'].split('left: ')[1].split(';')[0])) != int(float(leftCss) + 9)) and (
                    int(float(el['style'].split('left: ')[1].split(';')[0])) != leftCss or not soup.select('.TCJour')[
                course]):
                continue

            day = soup.select('.TCJour')[theDay].text.split(' ')

            # date
            dayDate = day[1]
            dayMonth = datetime.strptime(day[2], '%B').month
            weekday = day[0].lower()
            year = '20' + queried_date.split('/')[2]
            date = f"{dayDate}/{dayMonth}/{year}"

            # time
            start = el.select('.TChdeb')[0].text[:5]
            end = el.select('.TChdeb')[0].text[8:13]

            # other information
            subject = el.select('.TCase')[0].text.strip()
            professor = el.select('.TCProf')[0].text.split('<br>')[0].split('</span>')[1]
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
