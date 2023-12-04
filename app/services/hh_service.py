import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company, CompanyIn
from app.services.company_service import CompanyService


def get_page(url, **kwargs):
    params = {"text": kwargs.get("text"), "page": kwargs.get("page")}
    return httpx.get(url, params=params)


class HHService:
    def __init__(self, session: AsyncSession, company_service: CompanyService):
        self.session = session
        self.company_service = company_service
        self.hh_api_url = "https://api.hh.ru"
        self.vacancy_path = "/vacancies"

    async def create_companies_from_vacancy_search(
        self, logged_in_email: str, text="python"
    ):
        page_number = 0
        resp = get_page(
            self.hh_api_url + self.vacancy_path, text=text, page=page_number
        )
        while resp.status_code == 200:
            for vacancy in resp.json().get("items"):
                name = vacancy.get("employer").get("name")
                hh_id = vacancy.get("employer").get("id")
                result = await self.session.execute(
                    select(Company).where(Company.hh_employer_id == hh_id)
                )
                companies = result.scalars().all()
                if len(companies) == 0 and hh_id is not None:
                    _ = await self.company_service.create(
                        CompanyIn(name=name, hh_employer_id=hh_id), logged_in_email
                    )
            page_number += 1
            resp = get_page(
                self.hh_api_url + self.vacancy_path, text=text, page=page_number
            )
