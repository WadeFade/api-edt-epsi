def get_month(month: str):
    month = month.lower()
    if month == 'janvier':
        return '01'
    elif month == 'février':
        return '02'
    elif month == 'mars':
        return '03'
    elif month == 'avril':
        return '04'
    elif month == 'mai':
        return '05'
    elif month == 'juin':
        return '06'
    elif month == 'juillet':
        return '07'
    elif month == 'aout':
        return '08'
    elif month == 'septembre':
        return '09'
    elif month == 'octobre':
        return '10'
    elif month == 'novembre':
        return '11'
    elif month == 'décembre':
        return '12'
    else:
        raise ValueError('Unrecognized month name')
