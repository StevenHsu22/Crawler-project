import fnmatch
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
timenow = date.today()

def timechange(x):
    if fnmatch.fnmatch(x, '* 週前'):
        timecount = int(x[0:1])
        b = timenow - timedelta(weeks=timecount)
        return b.strftime('%Y-%m-%d')
    
    elif fnmatch.fnmatch(x, '* 個月前'):
        timecount = int(x[0:1])
        b = timenow - relativedelta(months=timecount)
        return b.strftime('%Y-%m-%d')
    
    else:
        return timenow.strftime('%Y-%m-%d')
