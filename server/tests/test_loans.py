from datetime import date


class TestGetLoans:
    def test_responds_with_all_loans(self, client):
        response = client.get("/api/loans")
        assert response.status_code == 200
        assert len(response.json()["loans"]) == 12


class TestGetOverdueLoans:
    def test_responds_with_only_the_socket_set_loan(self, client):
        overdue = client.get("/api/loans/overdue").json()["loans"]
        assert [loan["tool_id"] for loan in overdue] == [9]

    def test_every_overdue_loan_is_unreturned_and_past_due(self, client):
        today = date.today().isoformat()
        for loan in client.get("/api/loans/overdue").json()["loans"]:
            assert loan["returned_date"] is None
            assert loan["due_date"] < today
