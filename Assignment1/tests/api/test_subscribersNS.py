# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency

def test_get_subscriber_should_list_all_subscribers(client, agency):
    response = client.get("/subscriber/")

    assert response.status_code == 200

    parsed = response.get_json()
    assert len(parsed["subscriber"]) == len(agency.subscribers)

def test_add_subscriber(client, agency):
    subscriber_count_before = len(agency.subscribers)

    response = client.post("/subscriber/",
                           json= {"name": "Stefan",
                                "address": "Albrechts 6, 3961 Waldenstein"
                                    })

    assert response.status_code == 200

    assert len(agency.subscribers)  == subscriber_count_before +1
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]

    assert subscriber_response["name"] == "Stefan"
    assert subscriber_response["address"] == "Albrechts 6, 3961 Waldenstein"

def test_get_editor(client, agency):

    subscriber_1 = agency.subscribers[0]
    subscriber_id = subscriber_1.subscriber_id

    response = client.get(f"/subscriber/{subscriber_id}")
    assert response.status_code == 200

    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]

    assert subscriber_response["name"] == "Hans"
    assert subscriber_response["address"] == "Albrechts 5, Waldenstein 3961"


def test_update_subscriber(client, agency):

    response = client.post("/subscriber/",
                           json= {
                               "name": "Maria",
                               "address": "Grünbach 12, 3961 Waldenstein"
                           })
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    subscriber_id = subscriber_response["subscriber_id"]

    response_updated = client.post(f"/subscriber/{subscriber_id}",
                                    json= {
                                        "name": "Anita",
                                        "address": "Gmünd 1, 3030 Gmünd"
                                            })

    assert response_updated.status_code == 200

    subscriber_updated = response_updated.get_json()
    subscriber_updated_response = subscriber_updated["subscriber"]

    assert subscriber_updated_response["name"] == "Anita"
    assert subscriber_updated_response["address"] == "Gmünd 1, 3030 Gmünd"

def test_remove_subscriber(client, agency):
    response = client.post("/subscriber/",
                           json= {
                               "name": "Martin",
                               "address": "Gmünd 10, 3030 Gmünd"
                           })
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    subscriber_id = subscriber_response["subscriber_id"]
    subscriber_count_before = len(agency.subscribers)

    response_new = client.delete((f"/subscriber/{subscriber_id}"))
    response_2 = client.delete(f"/subscriber/213")



    assert response_new.status_code == 200
    assert len(agency.subscribers) == subscriber_count_before -1
    assert response_2.status_code == 404
    parsed=response_2.get_json()
    assert parsed == f"Subscriber with ID 213 was not found"


def test_subscribe_newspaper(client, agency):

    subscriber_1 = agency.subscribers[0]
    before = len(subscriber_1.newspaper_list)

    response = client.post(f"/subscriber/{subscriber_1.subscriber_id}/subscribe",
                           json={
                               "paper_id": 100
                           })

    assert response.status_code == 200
    parsed = response.get_json()

    assert parsed == "The subscriber subscribed this newspaper 100"

def test_subscribe_newspaper_error(client, agency):

    subscriber_1 = agency.subscribers[0]
    before = len(subscriber_1.newspaper_list)

    response = client.post(f"/subscriber/{subscriber_1.subscriber_id}/subscribe",
                           json={
                               "paper_id": 1
                           })

    assert response.status_code == 404
    parsed = response.get_json()
    assert parsed == f"Subscriber with ID {subscriber_1.subscriber_id} or newspaper with ID 1 was not found"

def test_subscribe_specialissue(client, agency):
    subscriber_1 = agency.subscribers[0]
    before = len(subscriber_1.newspaper_list)

    response = client.post(f"/subscriber/{subscriber_1.subscriber_id}/subscribe/special_issue",
                           json={
                               "paper_id": 100,
                               "issue_id": 1001
                           })

    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "The subscriber subscribed this issue 1001"

def test_subscribe_specialissue_error(client, agency):

    subscriber_1 = agency.subscribers[0]
    before = len(subscriber_1.newspaper_list)

    response = client.post(f"/subscriber/{subscriber_1.subscriber_id}/subscribe/special_issue",
                           json={
                               "paper_id": 10,
                               "issue_id": 1001
                           })

    assert response.status_code == 404
    parsed = response.get_json()
    assert parsed == "Subscriber, newspaper or issue was not found"

def test_get_missing_issues(client, agency):
    newspaper = client.post(f"/newspaper/",
                            json = {
                                "name": "Simpsons",
                                "frequency": 6,
                                "price": 10
                            })
    parsed = newspaper.get_json()
    newspaper_response = parsed["newspaper"]
    paper_id = newspaper_response["paper_id"]

    response_issue = client.post(f"/newspaper/{paper_id}/issue",
                json = {
                    "releasedate": "Weekly",
                    "number_of_pages": 10
                })

    response_subscriber = client.post("/subscriber/",
                                      json = {
                                          "name": "Tobias",
                                          "address": "Hibelungen"
                                      })
    parsed_sub = response_subscriber.get_json()
    sub_response = parsed_sub["subscriber"]
    subscriber_id = sub_response["subscriber_id"]
    response_subscribe =  client.post(f"/subscriber/{subscriber_id}/subscribe",
                                      json = {
                                          "paper_id": paper_id
                                      })
    response = client.get(f"/subscriber/{subscriber_id}/missingissues")

    assert response.status_code == 200
    parsed = response.get_json()
    issue_response = parsed["issues"]
    assert len(issue_response) == 1

def test_subscriber_stats(client,agency):

    subscriber = agency.subscribers[0]
    newspaper = agency.newspapers[0]

    response_add = client.post(f"/subscriber/{subscriber.subscriber_id}/subscribe",
                               json = {
                                   "paper_id": newspaper.paper_id
                               })
    response = client.get(f"/subscriber/{subscriber.subscriber_id}/stats")

    parsed = response.get_json()
    print(parsed)











