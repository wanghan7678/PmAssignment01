from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from domain.services.position_services import PositionServices
from domain.entities.position import Position
from infrastructure.util.util import json_str_to_date, to_float
from infrastructure.pmapi.pm_reader_impl import PmReaderImpl
from interface.serializers import ReportSerializer
import json

START_DATE = "2023-01-01"
END_DATE = "2024-11-10"


@api_view(["POST"])
def generate_report(request):
    data = str(request.body, encoding='utf-8')
    positions = create_positions_from_json(json_str=data)
    pm_reader = PmReaderImpl()
    ps = PositionServices(pm_reader=pm_reader, positions=positions)
    ps.fill_positions(target_currency="USD", start_date=json_str_to_date(START_DATE),
                      end_date=json_str_to_date(END_DATE))
    report = ps.create_report(json_str_to_date(START_DATE), json_str_to_date(END_DATE))
    serializer = ReportSerializer(report)
    return Response(serializer.data)


def create_positions_from_json(json_str: str) -> []:
    po_list = json.loads(json_str)
    positions = []
    for po in po_list:
        position = Position(id=po.get("id"), open_date=json_str_to_date(po.get("open_date")),
                            open_price=to_float(po.get("open_price")), quantity=po.get("quantity"))
        position.close_date = json_str_to_date(po.get("close_date"))
        position.close_price = to_float(po.get("close_price"))
        if position.close_price:
            position.is_open = False
        position.transaction_costs = po.get("transaction_costs")
        position.instrument_id = po.get("instrument_id")
        position.instrument_currency = po.get("instrument_currency")
        position.open_transaction_type = po.get("open_transaction_type")
        positions.append(position)
    return positions
