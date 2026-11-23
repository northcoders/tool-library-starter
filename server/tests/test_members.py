class TestGetMembers:
    def test_responds_with_all_members(self, client):
        response = client.get("/api/members")
        assert response.status_code == 200
        assert len(response.json()["members"]) == 6


class TestGetMemberById:
    def test_responds_with_the_member(self, client):
        member = client.get("/api/members/2").json()["member"]
        assert member["name"] == "Sam Okafor"

    def test_responds_with_404_for_unknown_id(self, client):
        response = client.get("/api/members/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Member not found"}

    def test_responds_with_400_for_non_integer_id(self, client):
        assert client.get("/api/members/abc").status_code == 400
