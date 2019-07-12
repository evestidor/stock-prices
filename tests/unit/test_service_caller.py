from rest_framework.request import Request

from src.services import ServiceCaller
from src.registry import AbstractServiceRegistry


class FakeRegistry(AbstractServiceRegistry):
    services = {'service1': 'http://service1/', 'service2': 'http://service2'}

    def resolve_host(self, name: str) -> str:
        return self.services[name]


class TestGetFullURL:
    def _get_full_url(self, request, service_name):
        caller = ServiceCaller.from_django_request(
            request, service_name, registry=FakeRegistry()
        )
        return caller._get_full_url()

    def test_when_service_has_ending_slash_returns_url(self, rf):
        request = Request(rf.get('/service1/path/'))
        result = self._get_full_url(request, 'service1')
        expected = 'http://service1/path/'
        assert expected == result

    def test_when_service_does_not_have_ending_slash_returns_url(self, rf):
        request = Request(rf.get('/service2/path/'))
        result = self._get_full_url(request, 'service2')
        expected = 'http://service2/path/'
        assert expected == result
