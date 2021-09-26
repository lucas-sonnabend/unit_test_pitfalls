from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.testclient import TestClient
from starlette.responses import PlainTextResponse
from starlette.requests import Request

from unittest.mock import MagicMock, AsyncMock

import pytest

# custom_middleware.py ####################################
class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):    
        response = await call_next(request)
        response.headers["CustomField"] = "bla"
        return response

# test_custom_middleware.py ###############################
async def endpoint_for_test(_):
    return PlainTextResponse("Test")

middleware = [Middleware(CustomHeaderMiddleware)]
routes = [Route("/test", endpoint=endpoint_for_test)]
app = Starlette(routes=routes, middleware=middleware)

@pytest.mark.asyncio
async def test_middleware_sets_field():
    client = TestClient(app)
    response = client.get("/test")
    assert response.headers["CustomField"] == "bla"
 
# test_custom_middleware_2.py##############################
@pytest.mark.asyncio
async def test_middleware_sets_response_header_field():
    middleware = CustomHeaderMiddleware(MagicMock(Starlette))
    response = await middleware.dispatch(
        MagicMock(Request),
        AsyncMock(return_value=PlainTextResponse("Test"))
    )
    assert response.headers["CustomField"] == "bla"