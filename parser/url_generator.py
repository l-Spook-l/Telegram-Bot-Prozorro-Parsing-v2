from options import status_data, procurement_type_data, regions_data


async def get_url(data):
    list_url = []
    for i in range(len(data)):
        filters = ''
        DK012_2015 = data[i]['ДК021:2015'].split(', ')
        Status = data[i]['Статус'].split(', ')
        Procurement_type = data[i]['Вид закупівлі'].split(', ')
        Region = data[i]['Регіон'].split(', ')

        if Status[0] != 'пропустити':
            for id in range(len(Status)):
                filters += f'&status%5B{id}%5D={status_data[Status[id]]}'

        if Procurement_type[0] != 'пропустити':
            for id in range(len(Procurement_type)):
                filters += f'&proc_type%5B{id}%5D={procurement_type_data[Procurement_type[id]]}'

        if DK012_2015[0] != 'пропустити':
            for id in range(len(DK012_2015)):
                filters += f'&cpv%5B{id}%5D={DK012_2015[id]}'

        if Region[0] != 'пропустити':
            filters += regions_data[Region[0]]

        url = f'https://prozorro.gov.ua/api/search/tenders?filterType=tenders{filters}'
        list_url.append(url)

    return list_url
