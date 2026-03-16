"""Unit tests for the policy evaluation module."""

from unittest.mock import Mock

import pytest

from pytfe._http import HTTPTransport
from pytfe.errors import InvalidRunIDError
from pytfe.models.policy_check import (
    PolicyCheck,
    PolicyCheckListOptions,
    PolicyStatus,
)
from pytfe.resources.policy_check import PolicyChecks


class TestPolicyChecks:
    """Test the PolicyChecks service class."""

    @pytest.fixture
    def mock_transport(self):
        """Create a mock HTTPTransport."""
        return Mock(spec=HTTPTransport)

    @pytest.fixture
    def policy_checks_service(self, mock_transport):
        """Create a PolicyChecks service with mocked transport."""
        return PolicyChecks(mock_transport)

    def test_list_validations(self, policy_checks_service):
        """Test list method with invalid task stage ID."""

        # Test empty run ID
        with pytest.raises(InvalidRunIDError):
            list(policy_checks_service.list(""))

        # Test None run ID
        with pytest.raises(InvalidRunIDError):
            list(policy_checks_service.list(None))

    def test_list_success_with_options(self, policy_checks_service, mock_transport):
        """Test successful iteration with custom pagination options."""

        mock_response_data = {
            "data": [
                {
                    "id": "polchk-9VYRc9bpfJEsnwum",
                    "type": "policy-checks",
                    "attributes": {
                        "result": {
                            "result": False,
                            "passed": 0,
                            "total-failed": 1,
                            "hard-failed": 0,
                            "soft-failed": 1,
                            "advisory-failed": 0,
                            "duration-ms": 0,
                            "sentinel": {},
                        },
                        "scope": "organization",
                        "status": "soft_failed",
                        "status-timestamps": {
                            "queued-at": "2017-11-29T20:02:17+00:00",
                            "soft-failed-at": "2017-11-29T20:02:20+00:00",
                        },
                        "actions": {"is-overridable": True},
                        "permissions": {"can-override": True},
                    },
                    "relationships": {
                        "run": {"data": {"id": "run-veDoQbv6xh6TbnJD", "type": "runs"}}
                    },
                    "links": {
                        "output": "/api/v2/policy-checks/polchk-9VYRc9bpfJEsnwum/output"
                    },
                }
            ]
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_transport.request.return_value = mock_response

        options = PolicyCheckListOptions(page_size=5)  # type: ignore
        result = policy_checks_service.list("run-123", options=options)

        # Verify the request was made with correct parameters
        assert mock_transport.request.call_count == 1
        call_args = mock_transport.request.call_args
        assert call_args[0][0] == "GET"
        assert call_args[0][1] == "/api/v2/runs/run-123/policy-checks"

        # Verify custom options were passed and merged with _list defaults
        params = call_args[1]["params"]
        assert params["page[size]"] == 5  # Custom value from options

        # Verify the result
        print(type(result))
        assert len(result.items) == 1
        assert isinstance(result.items[0], PolicyCheck)
        assert result.items[0].id == "polchk-9VYRc9bpfJEsnwum"
        assert result.items[0].status == PolicyStatus.POLICY_SOFT_FAILED
        assert result.items[0].result.advisory_failed == 0
        assert result.items[0].result.total_failed == 1

    def test_list_empty_result(self, policy_checks_service, mock_transport):
        """Test iteration with no results."""

        mock_response_data = {"data": []}

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_transport.request.return_value = mock_response

        result = policy_checks_service.list("run-empty")

        # Verify the request was made
        assert mock_transport.request.call_count == 1

        # Verify iterator yields no items
        assert len(result.items) == 0
        assert result.items == []
