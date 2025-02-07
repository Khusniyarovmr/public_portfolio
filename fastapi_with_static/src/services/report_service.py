from src.crud.message import message_crud


class ReportService:

    @staticmethod
    async def get_report(address: str):
        try:
            report_data = await message_crud.get_report_by_address(address=address)
            if len(report_data) > 100:
                return {"report_data": [("Слишком много данных для вывода. Выберите другой адрес",)]}
            report_data = [
                (row[0], row[1]) for row in report_data
            ]
        except Exception as e:
            print(e)
        else:
            return {"report_data": report_data}


report_service = ReportService()
