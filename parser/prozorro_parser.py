import aiohttp
from fake_useragent import UserAgent
from .url_generator import get_url

# urls = ["https://prozorro.gov.ua/api/search/tenders?filterType=tenders?region=7-9&status%5B0%5D=active.enquiries",]
# urls = ["https://prozorro.gov.ua/api/search/tenders?region=7-9&status%5B0%5D=active.enquiries",]


async def get_json(data_for_parser):
    user_agent = UserAgent()
    random_user_agent = user_agent.chrome
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": random_user_agent,
    }
    list_tenders = []
    list_data = []

    urls = await get_url(data_for_parser)
    for url in range(len(urls)):
        async with (aiohttp.ClientSession() as session):
            response = await session.post(url=urls[url], headers=headers)
            data = await response.json()
            quantity_tender_on_first_page = data['per_page']
            total_tenders = data["total"]

            if total_tenders >= 500:
                total_tenders = 500

            if total_tenders <= quantity_tender_on_first_page:
                page = 1
            else:
                page = total_tenders // quantity_tender_on_first_page + 1

            try:
                for item in range(1, page + 1):
                    url_page = f"{urls[url]}&page={item}"

                    async with session.post(url=url_page, headers=headers) as response_page:
                        data_page = await response_page.json()
                        for tender in range(len(data_page["data"])):
                            title = data_page["data"][tender]["title"]
                            city_company = data_page["data"][tender]["procuringEntity"]["address"].get("locality") or \
                                           data_page["data"][tender]["procuringEntity"]["address"].get("region") or \
                                           'Регіон не вказано або вказано не вірно'

                            name_company = data_page["data"][tender]["procuringEntity"]["identifier"].get(
                                "legalName") or data_page["data"][tender]["procuringEntity"].get("name") or \
                                           'Назву не вказано або вказано не вірно'

                            ID_tender = data_page["data"][tender]["tenderID"]
                            try:
                                price = data_page["data"][tender]["value"]["amount"]
                            except Exception as error:
                                price = 'Ціни ще немає'
                            try:
                                start_date = data_page["data"][tender]["enquiryPeriod"]["startDate"][:10]
                            except Exception as error:
                                start_date = 'Дати проведення ще немає'
                            link = (f"https://prozorro.gov.ua/tender/{ID_tender}")
                            list_tenders += [[title, city_company, name_company, ID_tender, price, start_date, link]]
                list_data.append({'list_tenders': list_tenders, 'total_tenders': total_tenders})
            except Exception as ex:
                print('Something went wrong')
                print(f'Error{ex}')
    return list_data
