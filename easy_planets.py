from datetime import datetime
import ephem

# Мы будем иметь дело с вводом живых пользователей. Чтобы не загружать их
# глупыми требованиями ввести 'Mars' точно без пробелов, именно в таком
# регистре, давайте разрешим им более неряшливый ввод.
def normalize_planet_name(raw_planet_name):
    aliases = {
        'mercury':  'Mercury',
        'меркурий': 'Mercury',

        'venus':  'Venus',
        'венера': 'Venus',

        'mars': 'Mars',
        'марс': 'Mars',

        'jupiter': 'Jupiter',
        'юпитер':  'Jupiter',

        'saturn':  'Saturn',
        'сатурн':  'Saturn',

        'uran':  'Uran',
        'уран':  'Uran',

        'neptune': 'Neptune',
        'нептун':  'Neptune',

        'pluto':  'Pluto',
        'плутон': 'Pluto',
    }

    not_normalized_planet_name = (str(raw_planet_name)).strip().lower()
    planet_name = aliases.get(not_normalized_planet_name, '')

    return planet_name

def get_ephem_planet(raw_planet_name):
    planet_name = normalize_planet_name(raw_planet_name);
    ephem_planet = None
    if hasattr(ephem, planet_name):
        ephem_planet = getattr(ephem, planet_name)()
    return ephem_planet

def get_current_ephem_datetime():
    # Мы хотим иметь на выходе дату в формате:
    # '1984/12/21 15:00' - должно быть время по UT0
    ephem_datetime = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')
    return ephem_datetime

def get_constellation_label_for_planet(ephem_planet):
    if ephem_planet == None:
        return ''

    ephem_datetime = get_current_ephem_datetime()
    ephem_planet.compute(ephem_datetime)

    constellation = ephem.constellation(ephem_planet)

    try:
        constellation_label = constellation[1]
    except IndexError:
        constellation_label = ''

    return constellation_label

# Набор тестов.
def main():
    datetime_for_ephem = get_current_ephem_datetime();
    print('Дата в формате, пригодном для PyEphem:')
    print(datetime_for_ephem)
    print('')

    raw_planet_name = str(input('Введите имя планеты: '))

    planet_name = normalize_planet_name(raw_planet_name)
    print('Нормализованное имя планеты:')
    print(planet_name)
    print('')

    ephem_planet = get_ephem_planet(raw_planet_name)
    print('Планета:')
    print(ephem_planet)
    print('')

    constellation_label = get_constellation_label_for_planet(ephem_planet)
    print('Созвездие:')
    print(constellation_label)
    print('')

if __name__ == "__main__":
    main()

# Интересно что при запуске main, подбрасывается предупреждение
# easy_planets.py:64: DeprecationWarning: PY_SSIZE_T_CLEAN will be required for '#' formats
# constellation = ephem.constellation(ephem_planet)
#
# Пока всё выглядит так как будто это происходит исключительно где-то в недрах
# библиотеки PyEphem. Вот пример с сайта этой библиотеки:
# https://rhodesmill.org/pyephem/
# import ephem
# mars = ephem.Mars()
# mars.compute('2007/10/02 00:50:22')
# ephem.constellation(mars)
# Что даёт такой результат:
# <stdin>:1: DeprecationWarning: PY_SSIZE_T_CLEAN will be required for '#' formats
# ('Gem', 'Gemini')
