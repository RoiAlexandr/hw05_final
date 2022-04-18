from datetime import datetime


# Добавляем текущий год в футер ключ {{year}}
def year(request):
    dt = datetime.now().year
    return {
        'year': dt
    }
