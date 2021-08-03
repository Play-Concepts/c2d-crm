from schemathesis import from_asgi

from app.main import app as application

schema = from_asgi("/api/openapi.json", application)


@schema.parametrize()
def test_api(case):
    response = case.call_asgi()
    case.validate_response(response)
