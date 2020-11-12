import datetime as dt


def year(request):
    year = dt.datetime.now().strftime('%Y')
    return {
        'year': year,
    }
