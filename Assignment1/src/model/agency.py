from typing import List
from .newspaper import Newspaper
from .subscriber import Subscriber
from .editor import Editor
from .issue import Issue
class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.subscribers: List[Subscriber] = []
        self.editors: List[Editor] = []

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def reset(self):
        self.newspapers = []
        self.subscribers = []
        self.editors = []

    @staticmethod
    def next_id(items, attribute_name):
        existing_ids = [
            getattr(item, attribute_name)
            for item in items
            if hasattr(item, attribute_name)
        ]
        if not existing_ids:
            return 1
        return max(existing_ids) + 1

    def add_newspaper(self, new_paper: Newspaper):
        #add newspaper if entered parameters are correct
        for paper in self.newspapers: # select one paper
            if paper.paper_id == new_paper.paper_id: # look for the same id
                raise ValueError(f"A newspaper with ID {new_paper.paper_id} already exists")
        self.newspapers.append(new_paper) # create a new paper


    def get_newspaper(self, paper_id):
        #could also raise an error of paper_id is nor correct
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)

    def update_newspaper(self, updated_newspaper: Newspaper):
        #did not check if the name already exists or other attributs because it makes no sense to me
        for i, newspaper in enumerate(self.newspapers):
            if newspaper.paper_id == updated_newspaper.paper_id:
                self.newspapers[i] = updated_newspaper
                return updated_newspaper
        return None

    def newspaper_stats(self, paper_id):
        count = 0
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                for subscriber in self.subscribers:
                    if paper in subscriber.newspaper_list:
                        count += 1
                    for special_issue in subscriber.specialissue_list:
                        count_list = []
                        if special_issue in [issue for issue in paper.issues]:
                            count_list.append(special_issue)
                            if len(count_list) > 0:
                                count += 1
                monthly_revenue = paper.price * count
                revenue = round((monthly_revenue * 12),2)
                return count, monthly_revenue, revenue
        return None

    def add_issue(self, new_issue: Issue, paper_id):
        # could raise an value error of issue id is the same should not happen with id()
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                for issue in paper.issues:
                    if issue.issue_id == new_issue.issue_id:
                        raise ValueError(f"An issue with ID {new_issue.issue_id} already exists")
                paper.issues.append(new_issue)
                return new_issue
        return None

    def get_all_issues(self, paper_id):
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper.issues
        return None

    def get_issue(self,paper_id, issue_id):
        # we basically go thorugh newspapers and issues and find the right issue and set its Boolean value to true
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                for issue in paper.issues:
                    if issue.issue_id == issue_id:
                        return issue
        return None


    def release_issue(self, paper_id, issue_id):
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                for issue in paper.issues:
                    if issue.issue_id == issue_id:
                        issue.released = True
                        return issue
        return None

    def add_subscriber(self, new_subscriber: Subscriber):
        #same as newspaper or addissue
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == new_subscriber.subscriber_id:
                raise ValueError(f"A subscriber with ID {new_subscriber.subscriber_id} already exists")
        self.subscribers.append(new_subscriber)

    def get_subscriber(self, subscriber_id):
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                return subscriber
        return None

    def all_subscriber(self) -> List[Subscriber]:
        return self.subscribers

    def remove_subscriber(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    def update_subscriber(self, updated_subscriber: Subscriber):
        # subscriber could also have same name or address
        for i, subscriber in enumerate(self.subscribers):
            if subscriber.subscriber_id == updated_subscriber.subscriber_id:
                self.subscribers[i] = updated_subscriber
                return updated_subscriber
        return None

    def subscribe_newspaper(self, subscriber_id, paper_id):
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                for paper in self.newspapers:
                    if paper.paper_id == paper_id:
                        if paper not in subscriber.newspaper_list:
                            subscriber.newspaper_list.append(paper)
                        return paper.paper_id
                return None
        return None

    def subscribe_special_issue(self,subscriber_id,  paper_id, issue_id):
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                for paper in self.newspapers:
                    if paper.paper_id == paper_id:
                        for issue in paper.issues:
                            if issue.issue_id == issue_id:
                                if issue not in subscriber.specialissue_list:
                                    subscriber.specialissue_list.append(issue)
                                return issue_id
                        return None
                return None
        return None

    def send_issue_subscriber(self, paper_id, issue_id):
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                for issue in paper.issues:
                    if issue.issue_id == issue_id:
                        issue.delivered = True
                        return issue
        return None

    def subscriber_stats(self, subscriber_id):
        #calculate the monthly price ad every nespaper price need to be individual because the price can be different
        #calculate annual costs = price * 12
        # get the number of issues look for the delivered issues in every newspaper and return the issues
        monthly_price = 0

        delivered_issues = []
        count = 0
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                len_paper = len(subscriber.newspaper_list)
                for paper in subscriber.newspaper_list:
                    monthly_price += paper.price
                    count += 1
                    for issue in paper.issues:
                        if  issue.delivered:
                            delivered_issues.append(issue)
                #in my opinion if sombody subscribes to a special_issue he needs to pay extra
                for special in subscriber.specialissue_list:
                    count += 1
                annual_cost = monthly_price * 12
                return monthly_price, annual_cost, len(delivered_issues), count
        return None


    def check_undelivered_issues(self,subscriber_id):
        #look for any undelivered issues - delivered = False
        target = None
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                target = subscriber
                break
        if target is None:
            return None

        undelivered_issues = []
        for newspaper in target.newspaper_list:
            for issue in newspaper.issues:
                if not issue.delivered:
                    undelivered_issues.append(issue)
        for issue in target.specialissue_list:
            if not issue.delivered and issue not in undelivered_issues:
                undelivered_issues.append(issue)
        return undelivered_issues

    def add_editor(self, new_editor: Editor):
        for editor in self.editors:
            if editor.editor_id == new_editor.editor_id:  # look for the same id
                raise ValueError(f"An editor with ID {new_editor.editor_id} already exists")
        self.editors.append(new_editor)

    def get_editor(self, editor_id):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None

    def all_editor(self) -> List[Editor]:
        return self.editors

    def remove_editor(self, editor: Editor):
        # in my opinion there should always be an editor for a newspaper thats why there should always be one editor
        if len(editor.paper_list) > 0:
            for paper in editor.paper_list:
                for issue in paper.issues:
                    if issue.editor == editor:
                        for editor_1 in self.editors:
                            if editor_1 != editor:
                                for newspaper in editor_1.paper_list:
                                    if newspaper == paper:
                                        editor.paper_list.remove(paper)
                                        issue.set_editor(editor_1)

            if len(editor.paper_list) != 0:
                raise Exception("This editor is the only one left in the agency")
        self.editors.remove(editor)
    def update_editor(self, updated_editor: Editor):
        for i, editor in enumerate(self.editors):
            if editor.editor_id == updated_editor.editor_id:
                updated_editor.paper_list = editor.paper_list
                self.editors[i] = updated_editor
                return updated_editor
        return None

    def specify_editor(self, paper_id, issue_id,editor_id):
            for editor in self.editors:
                if editor.editor_id == editor_id:
                    for paper in self.newspapers:
                        if paper.paper_id == paper_id:
                            for issue in paper.issues:
                                if issue.issue_id == issue_id:
                                    issue.set_editor(editor)
                                    if paper not in editor.paper_list:
                                        editor.paper_list.append(paper)
                                    return editor_id
            else:
                return None

    def get_list_newspaper_issue_editor(self, editor_id):
        issue_list = []
        for paper in self.newspapers:
            for issue in paper.issues:

                if issue.editor != None and issue.editor.editor_id == editor_id:
                    issue_list.append(issue)
        return issue_list
