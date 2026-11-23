from data.tools import tools


class TestGetTools:
    def test_responds_with_200(self, client):
        assert client.get("/api/tools").status_code == 200

    def test_responds_with_object_with_tools_key(self, client):
        body = client.get("/api/tools").json()
        assert isinstance(body, dict)
        assert isinstance(body["tools"], list)

    def test_returns_all_18_tools(self, client):
        assert len(client.get("/api/tools").json()["tools"]) == 18

    def test_each_tool_has_expected_shape(self, client):
        for tool in client.get("/api/tools").json()["tools"]:
            assert set(tool.keys()) == {"id", "name", "category", "description", "loan_period_days", "available"}


class TestGetToolById:
    def test_responds_with_the_tool(self, client):
        body = client.get("/api/tools/3").json()
        assert body == {"tool": tools[2]}

    def test_responds_with_404_for_unknown_id(self, client):
        response = client.get("/api/tools/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Tool not found"}

    def test_responds_with_400_for_non_integer_id(self, client):
        response = client.get("/api/tools/abc")
        assert response.status_code == 400
        assert response.json() == {"detail": "Bad request"}
