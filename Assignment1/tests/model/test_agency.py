import pytest

from ...src.model.newspaper import Newspaper
from ..fixtures import app, client, agency
from ...src.model.editor import Editor
from ...src.model.subscriber import Subscriber
from ...src.model.issue import Issue


##########
#Newspaper
##########
def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=998,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1


def test_add_newspaper_same_id_should_raise_error(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)

    with pytest.raises(ValueError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
        # this one should rais ean exception!
        agency.add_newspaper(new_paper2)

def test_get_newspaper(agency):
    new_paper = agency.newspapers[0]
    paper_id = new_paper.paper_id

    targeted_newspaper = agency.get_newspaper(paper_id)
    assert targeted_newspaper.name == "The New York Times"
    assert targeted_newspaper.frequency == 7
    assert targeted_newspaper.price == 13.14

def test_all_newspaper(agency):
    paper_len = len(agency.newspapers)
    all_newspapers = agency.all_newspapers()
    assert paper_len == len(all_newspapers)

def test_update_newspaper(agency):
    new_paper = Newspaper(paper_id=200,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    # first adding of newspaper should be okay
    updated_newspaper = Newspaper(paper_id=200,
                          name="Hallo",
                          frequency=63,
                          price=3)

    updated_newspaper = agency.update_newspaper(updated_newspaper)
    targeted_newspaper = agency.get_newspaper(200)
    assert targeted_newspaper.name == "Hallo"
    assert targeted_newspaper.frequency == 63
    assert targeted_newspaper.price == 3

def test_remove_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = agency.newspapers[-1]
    agency.remove_newspaper(new_paper)
    assert len(agency.newspapers) == before -1


def test_newspaper_stats(agency):
    newspaper = agency.newspapers[1]
    subscriber = agency.subscribers[0]
    agency.subscribe_newspaper(subscriber.subscriber_id, newspaper.paper_id)

    count, monthly_revenue, revenue = agency.newspaper_stats(newspaper.paper_id)

    assert count == 1
    assert monthly_revenue == 1.12
    assert revenue == 13.44

#######
#Issues
#######
def test_add_issue(agency):

    newspaper = agency.newspapers[0]
    new_issue = Issue(
        issue_id= 67,
        releasedate= "30.10.2023",
        number_of_pages = 10
    )

    before = len(newspaper.issues)
    paper_id = newspaper.paper_id
    agency.add_issue(new_issue, paper_id)

    assert len(agency.get_all_issues(paper_id)) == before +1

def test_get_all_issues(agency):
    newspaper_1 = agency.newspapers[0]
    paper_id = newspaper_1.paper_id
    issue_len = len(newspaper_1.issues)
    all_issues = agency.get_all_issues(paper_id)
    assert issue_len == len(all_issues)

def test_get_issue(agency):
    newspaper_1 = agency.newspapers[0]
    paper_id = newspaper_1.paper_id

    issue_1 = newspaper_1.issues[0]
    issue_id = issue_1.issue_id

    targeted_issue = agency.get_issue(paper_id, issue_id)

    assert targeted_issue.releasedate == "30.10.2003"
    assert  targeted_issue.number_of_pages == 10


def test_release_issue(agency):
    paper_1 = agency.newspapers[0]
    issue_1 = paper_1.issues[4]

    targeted_issue = agency.release_issue(paper_1.paper_id, issue_1.issue_id)

    assert targeted_issue.released == True

def test_send_issue_subscriber(agency):
    paper1 = agency.newspapers[0]
    issue1 = paper1.issues[5]

    targeted_issue = agency.send_issue_subscriber(paper1.paper_id, issue1.issue_id)

    assert targeted_issue.delivered == True

def specify_editor(agency):
    editor1 = agency.editors[0]
    paper1 = agency.newspapers[0]
    issue1 = paper1.issues[0]

    agency.specify_editor(paper1.paper_id,issue1.issue_id,editor1.editor_id)

    assert issue1.editor.name == "Christian"
    assert issue1.editor.address == "Albrechts 112, Waldenstein 3961"
    assert len(editor1.paper_list) == 1

###########
#Subscriber
###########

def test_add_subscriber(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(name = "Bernhard",
                                address = "Waldenstein 11, 3961 Waldenstein")
    new_subscriber.subscriber_id = 21
    new_subscriber.newspaper_list = []
    new_subscriber.specialissue_list = []

    agency.add_subscriber(new_subscriber)
    assert len(agency.subscribers) == before +1

def test_add_subscriber_same_id_should_raise_error(agency):
    before = len(agency.subscribers)
    new_subscribers = agency.subscribers[0]
    with pytest.raises(ValueError, match = "A subscriber with ID 301 already exists"):
        agency.add_subscriber(new_subscribers)

def test_all_subscribers(agency):
    subscriber_len = len(agency.subscribers)
    all_subscribers = agency.all_subscriber()

    assert subscriber_len == len(all_subscribers)

def test_get_subscriber(agency):

    new_subscriber = agency.subscribers[0]
    subscriber_id = new_subscriber.subscriber_id

    targeted_subscriber = agency.get_subscriber(subscriber_id)

    assert targeted_subscriber.name == "Hans"
    assert targeted_subscriber.address == "Albrechts 5, Waldenstein 3961"

def test_update_subscriber(agency):

    new_subscriber = Subscriber(name="Michael",
                                address = "Gmünd 17, 3030 Gmünd")
    new_subscriber.subscriber_id = 888
    new_subscriber.newspaper_list = []
    new_subscriber.specialissue_list = []
    agency.add_subscriber(new_subscriber)

    updated_subscriber = Subscriber(name="Manuel",
                                    address = "Nondorf 1, 3961 Waldenstein")
    updated_subscriber.subscriber_id = 888
    updated_subscriber.newspaper_list = []
    updated_subscriber.specialissue_list = []

    updated_subscriber = agency.update_subscriber(updated_subscriber)
    targeted_subscriber = agency.get_subscriber(888)

    assert targeted_subscriber.name == "Manuel"
    assert targeted_subscriber.address == "Nondorf 1, 3961 Waldenstein"

def test_remove_subscriber(agency):
    before = len(agency.subscribers)
    new_subscriber = agency.subscribers[0]
    agency.remove_subscriber(new_subscriber)
    assert len(agency.subscribers) == before -1

def test_subscribe_newspaper(agency):
    paper_1 = agency.newspapers[0]
    subscriber_1 = agency.subscribers[0]

    agency.subscribe_newspaper(subscriber_1.subscriber_id, paper_1.paper_id)

    assert subscriber_1.newspaper_list[0].name == "The New York Times"
    assert subscriber_1.newspaper_list[0].frequency == 7
    assert subscriber_1.newspaper_list[0].price == 13.14

def test_subscribe_special_issue(agency):
    paper_1 = agency.newspapers[0]
    subscriber_1 = agency.subscribers[0]
    issue1 = paper_1.issues[0]

    agency.subscribe_special_issue(subscriber_1.subscriber_id, paper_1.paper_id, issue1.issue_id)

    assert subscriber_1.specialissue_list[0].releasedate == "30.10.2003"
    assert subscriber_1.specialissue_list[0].number_of_pages == 10

def test_check_undelivered_issues(agency):
    new_subscriber = Subscriber(name = "Tobias", address = "Lazy Town")
    new_subscriber.subscriber_id = 12344
    new_subscriber.newspaper_list = []
    new_subscriber.specialissue_list = []
    agency.add_subscriber(new_subscriber)
    new_paper = Newspaper(paper_id= 1234567, name = "Standard", frequency = 5 , price = 10)
    agency.add_newspaper(new_paper)
    issue = Issue(issue_id = 12345599, releasedate = "daily", number_of_pages= 10)
    agency.add_issue(issue, new_paper.paper_id)
    target = agency.subscribe_newspaper(new_subscriber.subscriber_id, new_paper.paper_id)
    print(target)
    result = agency.check_undelivered_issues(new_subscriber.subscriber_id)
    print(result)
    assert len(result) == 1
    assert result[0].releasedate == "daily"
    assert result[0].number_of_pages == 10

def test_subscriber_stats(agency):
    subscriber = agency.subscribers[0]
    newspaper = agency.newspapers[0]

    agency.subscribe_newspaper(subscriber.subscriber_id, newspaper.paper_id)
    monthly_price, annual_cost, number_issues, count = agency.subscriber_stats(subscriber.subscriber_id)

    assert monthly_price == 13.14
    assert annual_cost == 157.68
    assert number_issues == 0
    assert count == 1

########
#editor
#######
def test_all_editor(agency):
    editor_len = len(agency.editors)
    all_editors = agency.all_editor()
    assert editor_len == len(all_editors)


def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(name = "Alex",
                        address = "Albrechts 112")
    new_editor.editor_id = 991
    new_editor.paper_list = []
    agency.add_editor(new_editor)
    assert len(agency.all_editor()) == before +1

def test_add_editor_same_id_should_raise_error(agency):
    before = len(agency.editors)
    new_editor = agency.editors[0]
    with pytest.raises(ValueError, match = "An editor with ID 202 already exists"):
        agency.add_editor(new_editor)

def test_get_editor(agency):
    new_editor = agency.editors[0]
    editor_id = new_editor.editor_id

    targeted_editor = agency.get_editor(editor_id)

    assert targeted_editor.name == "Christian"
    assert targeted_editor.address == "Albrechts 112, Waldenstein 3961"

def test_update_editor(agency):
    new_editor = Editor(name = "Erwin",
                        address = "Albrechts 113")
    new_editor.editor_id = 30
    new_editor.paper_list = []

    agency.add_editor(new_editor)
    updated_editor = Editor(name = "Alex",
                            address = "Albrechts 100")
    updated_editor.editor_id = 30
    new_editor.paper_list = []

    updated_editor = agency.update_editor(updated_editor)
    targeted_editor = agency.get_editor(30)
    assert targeted_editor.name == "Alex"
    assert targeted_editor.address == "Albrechts 100"

def test_remove_editor(agency):


    editor1 = Editor(name = "Mozart", address="Lazy Town")
    editor1.paper_list = []
    editor1.editor_id = 17879879
    agency.add_editor(editor1)
    before = len(agency.editors)
    agency.remove_editor(editor1)
    assert len(agency.editors) == before - 1

def test_remove_editor_exception(agency):

    editor1 = Editor(name = "Dominik", address="Lazy Town")
    editor1.paper_list = []
    editor1.editor_id = 17879878
    agency.add_editor(editor1)
    editor2 = Editor(name="Franz", address="Lazy Town")
    editor2.paper_list = []
    editor2.editor_id = 17879820
    agency.add_editor(editor2)
    newspaper = Newspaper(paper_id= 12310, name = "Presse", frequency = 5 , price = 10)
    agency.add_newspaper(newspaper)
    issue1 = Issue(issue_id=12345530, releasedate="daily", number_of_pages=10)
    agency.add_issue(issue1, newspaper.paper_id)
    issue2 = Issue(issue_id=12345555, releasedate="weekly", number_of_pages=10)
    agency.add_issue(issue2, newspaper.paper_id)
    agency.specify_editor(newspaper.paper_id, issue1.issue_id, editor1.editor_id)
    agency.specify_editor(newspaper.paper_id, issue2.issue_id, editor2.editor_id)
    for editor in agency.editors:
        print(editor.paper_list)
    #agency.remove_editor(editor1)
    #assert issue1.editor.name == "Franz"
    #assert issue2.editor.name == "Franz"
def test_get_list_newspaper_issue_editor(agency):
    editor = agency.editors[1]
    paper1 = agency.newspapers[0]
    issue = paper1.issues[0]

    before = len(editor.paper_list)
    agency.specify_editor(paper1.paper_id, issue.issue_id, editor.editor_id)
    after = agency.get_list_newspaper_issue_editor(editor.editor_id)

    assert len(after) == before + 1













