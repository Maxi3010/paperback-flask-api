from ..src.model.agency import Agency
from ..src.model.newspaper import Newspaper
from ..src.model.editor import Editor
from ..src.model.subscriber import Subscriber
from ..src.model.issue import Issue
def create_newspapers(agency: Agency):
    paper1 = Newspaper(paper_id=100, name="The New York Times", frequency=7, price=13.14)
    paper2 = Newspaper(paper_id=101, name="Heute", frequency=1, price=1.12)
    paper3 = Newspaper(paper_id=115, name="Wall Street Journal", frequency=1, price=3.00)
    paper4 = Newspaper(paper_id=125, name="National Geographic", frequency=30, price=34.00)



    issue1 = Issue(issue_id = 1000, releasedate= "30.10.2003", number_of_pages= 10)
    issue2 = Issue(issue_id=1001, releasedate="10.10.2003", number_of_pages=9)
    issue3 = Issue(issue_id=1020, releasedate="20.10.2003", number_of_pages=20)
    issue4 = Issue(issue_id=1030, releasedate="15.10.2003", number_of_pages=15)
    issue5 = Issue(issue_id = 1040, releasedate = "Weekly", number_of_pages= 11, released = False, delivered = False)
    issue6 = Issue(issue_id = 1050, releasedate = "Monthly", number_of_pages= 12, released = False, delivered = False)
    issue7 = Issue(issue_id = 1100, releasedate="every5days", number_of_pages= 4, released= False, delivered= False)
    paper1.issues.append(issue1)
    paper1.issues.append(issue2)
    paper1.issues.append(issue3)
    paper1.issues.append(issue4)
    paper1.issues.append(issue5)
    paper1.issues.append(issue6)
    paper3.issues.append(issue7)
    agency.newspapers.extend([paper1, paper2, paper3, paper4])

def create_editor(agency: Agency):
    editor1 = Editor(name="Christian", address="Albrechts 112, Waldenstein 3961")
    editor2 = Editor(name="Maximilian", address="Waldenstein 55, Waldenstein 3961")
    editor3 = Editor(name="James", address="Albrechts 100, Waldenstein 3961")
    editor4 = Editor(name="David", address="Albrechts 1, Waldenstein 3961")
    editor1.editor_id = 202
    editor2.editor_id = 203
    editor3.editor_id = 205
    editor4.editor_id = 215
    editor1.paper_list = []
    editor2.paper_list = []
    editor3.paper_list = []
    editor4.paper_list = []
    agency.editors.extend([editor1, editor2, editor3, editor4])


def create_subscriber(agency: Agency):
    subscriber1 = Subscriber(name="Hans", address = "Albrechts 5, Waldenstein 3961")
    subscriber2 = Subscriber(name="David", address= "Waldenstein 5, Waldenstein 3961")
    subscriber3 = Subscriber(name="Alex", address="Albrechts 2, Waldenstein 3961")
    subscriber4 = Subscriber(name="Christopher", address="Waldenstein 6, Waldenstein 3961")
    subscriber1.subscriber_id = 301
    subscriber2.subscriber_id = 302
    subscriber3.subscriber_id = 303
    subscriber4.subscriber_id = 305
    subscriber1.newspaper_list = []
    subscriber2.newspaper_list = []
    subscriber3.newspaper_list = []
    subscriber4.newspaper_list = []
    subscriber1.specialissue_list = []
    subscriber2.specialissue_list = []
    subscriber3.specialissue_list = []
    subscriber4.specialissue_list = []
    agency.subscribers.extend([subscriber1, subscriber2, subscriber3, subscriber4])

def populate(agency: Agency):
    create_newspapers(agency)
    create_editor(agency)
    create_subscriber(agency)


