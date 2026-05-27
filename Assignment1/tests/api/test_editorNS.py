#import the fixtures (this is necessary!)
from ..fixtures import app, client, agency

def test_get_editor_should_list_all_editors(client, agency):
    # send request
    response = client.get("/editor/")

    # test status code

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["editors"]) == len(agency.editors)

def test_add_editor(client, agency):
    editor_count_before = len(agency.editors)

    response = client.post("/editor/",
                           json= {
                               "name": "Stefan",
                               "address": "Grünbach 100, 3961 Waldenstein"
                           })

    assert response.status_code == 200

    assert len(agency.editors) == editor_count_before + 1
    parsed = response.get_json()
    editor_response = parsed["editor"]

    # verify that the response contains the editor data
    assert editor_response["name"] == "Stefan"
    assert editor_response["address"] == "Grünbach 100, 3961 Waldenstein"

def test_get_editor(client, agency):
    editor_1 = agency.editors[0]
    editor_id = editor_1.editor_id

    response = client.get(f"/editor/{editor_id}")
    assert response.status_code == 200

    parsed = response.get_json()
    editor_response = parsed["editor"]

    assert editor_response["name"] == "Christian"
    assert editor_response["address"] == "Albrechts 112, Waldenstein 3961"

def test_update_editor(client, agency):

    response = client.post("/editor/",
                           json={
                               "name": "Magdalena",
                               "address": "Albrechts 5, Waldenstein 3961"
                           })
    parsed = response.get_json()
    editor_response = parsed["editor"]
    editor_id = editor_response["editor_id"]

    response_updated = client.post(f"/editor/{editor_id}",
                                   json={
                                       "name": "Alexandra",
                                       "address": "Grünbach 10, 3961 Waldenstein"
                                   })

    assert response_updated.status_code == 200

    editor_updated = response_updated.get_json()
    editor_updated_response = editor_updated["editor"]

    assert editor_updated_response["name"] == "Alexandra"
    assert editor_updated_response["address"] == "Grünbach 10, 3961 Waldenstein"

def test_remove_editor(client, agency):
    response = client.post("/editor/",
                           json={
                               "name": "Magdalena",
                               "address": "Albrechts 5, Waldenstein 3961"
                           })
    parsed = response.get_json()
    editor_response = parsed["editor"]
    editor_id = editor_response["editor_id"]
    editor_count_before = len(agency.editors)

    response_new = client.delete((f"/editor/{editor_id}"))
    response_2 = client.delete(f"/editor/124")

    assert response_new.status_code == 200
    assert len(agency.editors) == editor_count_before -1
    assert  response_2.status_code == 404
    parsed = response_2.get_json()
    assert parsed == f"Editor with ID 124 was not found"
    response = client.delete(f"/editor/{editor_id}")
    response_2 = client.delete(f"/editor/123")
    assert response.status_code == 404
    assert len(agency.editors) == editor_count_before - 1
    assert response.get_json() == f"Editor with ID {editor_id} was not found"
    assert response_2.status_code == 404
    parsed = response_2.get_json()
    assert parsed == f"Editor with ID 123 was not found"

def test_get_editor_issues(client, agency):
    editor_1 = agency.editors[0]
    newspaper_1 = agency.newspapers[0]
    issue = newspaper_1.issues[0]
    before = len(editor_1.paper_list)
    response_set_editor = client.post(f"/newspaper/{newspaper_1.paper_id}/issue/{issue.issue_id}/editor",
                           json = {
                               "editor_id": 202
                           })

    response_get_issues = client.get(f"/editor/{editor_1.editor_id}/issues")
    assert response_get_issues.status_code == 200

    parsed = response_get_issues.get_json()
    issue_response = parsed["issues"]

    assert len(issue_response) == before +1










