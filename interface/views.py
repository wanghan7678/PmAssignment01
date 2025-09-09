from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from domain.services.position_services import PositionServices, create_positions_from_json
from infrastructure.util.util import json_str_to_date, to_float
from infrastructure.pmapi.pm_reader_impl import PmReaderImpl
from interface.serializers import ReportSerializer
import json

START_DATE = "2023-01-01"
# START_DATE = "2024-11-01"
END_DATE = "2024-11-10"


@api_view(["POST"])
def generate_report(request):
    data = str(request.body, encoding='utf-8')
    pm_reader = PmReaderImpl()
    ps = PositionServices(pm_reader=pm_reader)
    ps.load_from_json(data)
    ps.fill_positions(target_currency="USD", start_date=json_str_to_date(START_DATE),
                      end_date=json_str_to_date(END_DATE))
    report = ps.create_report(json_str_to_date(START_DATE), json_str_to_date(END_DATE))
    serializer = ReportSerializer(report)
    return Response(serializer.data)



