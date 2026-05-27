
class Issue(object):
    #every issue has this attributes which are needed to describe the issue
    def __init__(self, releasedate, number_of_pages, issue_id,  released: bool = False, delivered: bool = False):
        self.releasedate = releasedate
        self.released: bool = released
        self.editor = None
        self.number_of_pages = number_of_pages
        self.issue_id = issue_id
        self.delivered: bool = delivered
    def set_editor(self, editor):
        # this method is used for specifying an editor to an issue
        self.editor = editor

