status_data = {
    'період уточнень': 'active.enquiries',
    'подання пропозицій': 'active.tendering',
    'кваліфікація': 'active.pre-qualification',
    'кваліфікація (період оскарження)': 'active.pre-qualification.stand-still',
    'аукціон': 'active.auction',
    'визначення переможця': 'active.qualification',
    'визначення переможця (період оскарження)': 'active.qualification.stand-still',
    'пропозиції розглянуті': 'active.awarded',
    'торги не відбулися': 'unsuccessful',
    'торги відмінено': 'cancelled',
    'завершена': 'complete',
    'підготовка угоди': 'active',
    'підготовка до 2-го етапу': 'active.stage2.pending',
    'створення 2-го етапу': 'active.stage2.waiting',
}


procurement_type_data = {
    'спрощена закупівля': 'belowThreshold',
    'відкриті торги з особливостями': 'aboveThreshold',
    'тендер': 'competitiveOrdering',
    'відкриті торги': 'aboveThresholdUA',
    'відкриті торги з публікацією англійською мовою': 'aboveThresholdEU',
    'переговорна процедура': 'negotiation',
    'переговорна процедура (скорочена)': 'negotiation.quick',
    'переговорна процедура для потреб оборони': 'aboveThresholdUA.defense',
    'конкурентний діалог 1-ий етап': 'competitiveDialogueUA',
    'конкурентний діалог з публікацією англійською мовою 1-ий етап': 'competitiveDialogueEU',
    'конкурентний діалог 2-ий етап': 'competitiveDialogueUA.stage2',
    'конкурентний діалог з публікацією англійською мовою 2-ий етап': 'competitiveDialogueEU.stage2',
    'закупівля без використання електронної системи': 'reporting',
    'відкриті торги для закупівлі енергосервісу': 'esco',
    'укладання рамкової угоди': 'closeFrameworkAgreementUA',
    'відбір для закупівлі за рамковою угодою': 'closeFrameworkAgreementSelectionUA',
    'запит ціни пропозицій': 'priceQuotation',
    'спрощені торги із застосуванням електронної системи закупівель': 'simple.defense',
}

regions_data = {
    'севастополь': '&region=99',
    'луганська область': '&region=91-94',
    'місто київ': '&region=1-6',
    'запорізька область': '&region=69-72',
    'харківська область': '&region=61-64',
    'дніпропетровська область': '&region=49-53',
    'полтавська область': '&region=36-39',
    'донецька область': '&region=83-87',
    'київська область': '&region=7-9',
    'одеська область': '&region=65-68',
    'херсонська область': '&region=73-75',
    'миколаївська область': '&region=54-57',
    'житомирська область': '&region=10-13',
    'волинська область': '&region=43-45',
    'львівська область': '&region=79-82',
    'чернівецька область': '&region=58-60',
    'черкаська область': '&region=18-20',
    'сумська область': '&region=40-42',
    'крим': '&region=95-98',
    'кіровоградська область': '&region=25-28',
    'закарпатська область': '&region=88-90',
    'хмельницька область': '&region=29-32',
    'чернігівська область': '&region=14-17',
    'тернопільська область': '&region=46-48',
    'івано-франківська область': '&region=76-78',
    'вінницька область': '&region=21-24',
    'рівненська область': '&region=33-35',
}
