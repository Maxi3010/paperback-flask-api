# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency

##########
#Newspaper
##########
# for all tests I used fixtures and created new data in order to practice testing. I also wanted to ensure I can use both for my tests
# The cleaner way would be to use either testdata or create new in the tests
def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14

def test_get_newspaper(client, agency):
    #prepaer
    newspaper_1 = agency.newspapers[0]
    paper_id = newspaper_1.paper_id
    #act
    response = client.get(f"/newspaper/{paper_id}")  # <-- note the slash at the end
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "The New York Times"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 13.14

def test_update_newspaper(client, agency):

    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 8,
                               "price": 3
                           })
    parsed = response.get_json()
    newspaper_response = parsed["newspaper"]
    paper_id = newspaper_response["paper_id"]

    response_updated = client.post(f"/newspaper/{paper_id}",
                              json={
                                  "name": "The New York Times",
                                  "frequency": 7,
                                  "price": 3.14
                              })
    assert response_updated.status_code == 200

    newspaper_updated = response_updated.get_json()
    newspaper_updated_response = newspaper_updated["newspaper"]

    assert newspaper_updated_response["name"] == "The New York Times"
    assert newspaper_updated_response["frequency"] == 7
    assert newspaper_updated_response["price"] == 3.14
def test_remove_newspaper(client, agency):
    newspaper_1 = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    parsed = newspaper_1.get_json()
    newspaper_response = parsed["newspaper"]
    paper_id = newspaper_response["paper_id"]
    paper_count_before = len(agency.newspapers)
    response = client.delete(f"/newspaper/{paper_id}")

    assert response.status_code == 200
    assert len(agency.all_newspapers()) == paper_count_before -1



def test_remove_newspaper_error(client, agency):

    response_2 = client.delete(f"/newspaper/123")
    assert response_2.status_code == 404
    parsed = response_2.get_json()
    assert parsed == f"Newspaper with ID 123 was not found"

def test_add_issue(client,agency):
    newspaper = agency.newspapers[2]
    issue_count_before = len(newspaper.issues)
    paper_id = newspaper.paper_id
    issue = client.post(f"/newspaper/{paper_id}/issue",
                        json ={
                            'releasedate': "12.10.2003",
                            'number_of_pages': 10,
                        })



    parsed_issue=issue.get_json()
    issue_response = parsed_issue["issue"]
    print(parsed_issue)
    issues = client.get(f"/newspaper/{paper_id}/issue")
    parsed = issues.get_json()
    issues_response = parsed["issues"]
    print(issues_response)
    assert len(issues_response) == issue_count_before + 1

    assert issue_response["releasedate"] == "12.10.2003"
    assert issue_response["number_of_pages"] == 10

def test_add_issue_error(client, agency):
    paper1 = agency.newspapers[0]
    before = len(paper1.issues)

    response = client.post(f"/newspaper/{paper1.paper_id}/issue",
                           json={
                               "releasedate": "Weekly",
                               "numberofpages": 7
                           })

    assert len(paper1.issues) == before

    #assert response.status_code == 500

def test_get_all_issue(client,agency):
    newspaper = agency.newspapers[0]
    paper_id = newspaper.paper_id

    issue_len = len(newspaper.issues)

    response = client.get(f"/newspaper/{paper_id}/issue")  # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["issues"]) == issue_len


def test_get_issue(client, agency):
    newspaper_1 = agency.newspapers[0]
    paper_id = newspaper_1.paper_id

    issue_1 = newspaper_1.issues[0]
    issue_id = issue_1.issue_id

    response = client.get(f"/newspaper/{paper_id}/issue/{issue_id}")
    assert response.status_code == 200

    parsed = response.get_json()
    issue_response = parsed["issue"]

    assert issue_response["releasedate"] == "30.10.2003"
    assert issue_response["number_of_pages"] == 10

def test_release_issue(client, agency):
    #arrange # get issue, check if values are correct
    paper_1 = agency.newspapers[0]
    issue1 = paper_1.issues[0]
    response = client.post(f"/newspaper/{paper_1.paper_id}/issue/{issue1.issue_id}/release")
    assert response.status_code == 200

    # act
    parsed = response.get_json()
    issue_response = parsed["issue"]

    #assert
    assert issue_response["releasedate"] == "30.10.2003"
    assert issue_response["number_of_pages"] == 10
    assert issue_response["released"] == True

def test_deliver_issue(client, agency):
    paper_1 = agency.newspapers[0]
    issue_1 = paper_1.issues[4]

    response = client.post(f"/newspaper/{paper_1.paper_id}/issue/{issue_1.issue_id}/deliver")

    assert response.status_code == 200

    parsed = response.get_json()
    issue_response = parsed["issue"]

    assert issue_response["delivered"] == True

def test_newspaper_stats(client, agency):
    paper1 = agency.newspapers[0]
    subscriber_1 = agency.subscribers[0]
    response = client.post(f"/subscriber/{subscriber_1.subscriber_id}/subscribe",
                           json = {
                               "paper_id": 100})

    response = client.get(f"/newspaper/{paper1.paper_id}/stats")

    assert  response.status_code == 200
    parsed = response.get_json()

    assert parsed == "Number of subscribers 1, Monthly price 13.14 and annual revenue 157.68"

def test_specify_editor(client, agency):
    paper_1 = agency.newspapers[0]
    issue1 = paper_1.issues[0]
    response = client.post(f"/newspaper/{paper_1.paper_id}/issue/{issue1.issue_id}/editor",
                           json={
                               "editor_id": 202
                           })

    assert response.status_code == 200

    parsed = response.get_json()
    assert  parsed == "The issue was specified this editor 202"


