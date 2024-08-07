import aiofiles
from .prozorro_parser import get_json


async def create_file_HTML(index: int, data: list):
    async with aiofiles.open(f"index_{index}.html", 'w', encoding='utf-8') as file:
        await file.write(' '.join(data))


async def create_HTML(data_for_parser: list):
    data = await get_json(data_for_parser)

    for i in range(len(data)):
        """"HTML file template"""
        List_HTML_for_email = ['<!doctype html>\n', '<html lang="en">\n', '<head>\n', '    <meta charset="UTF-8">\n',
                               '    <meta name="viewport"\n',
                               '          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">\n',
                               '    <meta http-equiv="X-UA-Compatible" content="ie=edge">\n',
                               '    <title>Document</title>\n', '</head>\n', '<body>\n', '\n', '</body>\n', '</html>']

        line = 0
        List_HTML_for_email.insert(10 + line, f"<p>Загальна кількість тендерів: <span>{data[i]['total_tenders']}</span></p>\n")
        for item in range(data[i]['total_tenders']):
            List_HTML_for_email.insert(11 + line, '<hr align="left" width="30%" color="black" size=1>\n')
            List_HTML_for_email.insert(12 + line, f'<p><a href="{data[i]["list_tenders"][item][6]}">{data[i]["list_tenders"][item][0]}</a></p>\n')
            List_HTML_for_email.insert(13 + line, f'<p>Місто: {data[i]["list_tenders"][item][1]}</p>\n')
            List_HTML_for_email.insert(14 + line, f'<p><strong>Компанія: </strong>{data[i]["list_tenders"][item][2]}</p>\n')
            List_HTML_for_email.insert(15 + line, f'<p><strong>ID: </strong>{data[i]["list_tenders"][item][3]}</p>\n')
            List_HTML_for_email.insert(16 + line, f'<p>Очікувана вартість: <strong>{data[i]["list_tenders"][item][4]} UAH</strong></p>\n')
            List_HTML_for_email.insert(17 + line, f'<p>Оголошено: {data[i]["list_tenders"][item][5]}</p>\n')
            line += 7

        await create_file_HTML(i + 1, List_HTML_for_email)
