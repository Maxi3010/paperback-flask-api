from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from ..model.agency import Agency
from ..model.issue import Issue
from ..model.newspaper import Newspaper

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

# models for the interface

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })

issue_model = newspaper_ns.model('IssueModel', {
    'issue_id': fields.Integer(required = False,
                help = "The unique identifier of an issue"),
    'releasedate': fields.String(required=True,
                help='The publication date of the issue in ISO format (YYYY-MM-DD)'),
    'number_of_pages': fields.Integer(required=True,
                help='The number of pages in the issue'),
    'released': fields.Boolean(required=False,
                help='Released status of this issue'),
    'delivered': fields.Boolean(required=False,
                help = "Delivered status of this issue")
})

specify_editor_model = newspaper_ns.model("SetEditorModel", {
    "editor_id": fields.Integer(required = True,
                help = "The unique identifier of an editor")
})
@newspaper_ns.route('/')
#@newspaper_ns.route(”/{Erweiterungen der Standardroute}”) - shows an specific function in the swagger
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper") #@newspaper_ns.doc(description = description of the route which I want to implement
    @newspaper_ns.expect(paper_model, validate=True) # used to show the returned value in a specific model - mostly json objects
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        agency = Agency.get_instance()
        # create a new paper object and add it
        new_paper = Newspaper(paper_id=Agency.next_id(agency.newspapers, "paper_id"),
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        agency.add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        if not search_result:
            newspaper_ns.abort(404, f"Newspaper with ID {paper_id} was not found")
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):

        #find the newspaper by ID
        agency = Agency.get_instance()
        newspaper = agency.get_newspaper(paper_id)
        if not newspaper:
            newspaper_ns.abort(404, f"Newspaper with ID {paper_id} was not found")

        updated_paper = Newspaper(paper_id = newspaper.paper_id, name = newspaper.name, frequency = newspaper.frequency, price = newspaper.price)
        #update newspaper data
        updated_paper.name = newspaper_ns.payload["name"]
        updated_paper.frequency = newspaper_ns.payload["frequency"]
        updated_paper.price = newspaper_ns.payload["price"]

        agency.update_newspaper(updated_paper)
        return updated_paper

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return f"Newspaper with ID {paper_id} was not found", 404
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")

@newspaper_ns.route('/<int:paper_id>/issue')
class Newspaperissues(Resource):

    @newspaper_ns.doc(issue_model, description="Add a new issue")  # @newspaper_ns.doc(description = “Beschreibung von der Route die man implementieren will”)
    @newspaper_ns.expect(issue_model,validate=True)  # um einen bestimmten input im Format des parameters vorzugeben, paper_model ist ein json object in diesem oder ähnlichen Format:
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):
        agency = Agency.get_instance()
        if not agency.get_newspaper(paper_id):
            newspaper_ns.abort(404, f"Newspaper with ID {paper_id} was not found")

        # create a new paper object and add it
        all_issue_ids = [issue for paper in agency.newspapers for issue in paper.issues]
        new_issue = Issue(issue_id = Agency.next_id(all_issue_ids, "issue_id"),
                          releasedate = newspaper_ns.payload["releasedate"],
                          number_of_pages = newspaper_ns.payload["number_of_pages"])
        agency.add_issue(new_issue, paper_id)

        # return the new paper
        return new_issue

    @newspaper_ns.doc(description="List all issues of a specific newspaper")
    @newspaper_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, paper_id):
        # Get the newspaper object by paper_id
        issues = Agency.get_instance().get_all_issues(paper_id)
        if issues is None:
            newspaper_ns.abort(404, f"Newspaper with ID {paper_id} was not found")
        return issues



@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class Newspaper_issue_information(Resource):
    @newspaper_ns.doc(description="List an issue of a specific newspaper")
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def get(self, paper_id, issue_id):
        issue = Agency.get_instance().get_issue(paper_id, issue_id)
        if not issue:
            newspaper_ns.abort(404, f"Issue with ID {issue_id} was not found")
        return issue



@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class Newspaper_release(Resource):

    @newspaper_ns.doc(description= "Release an issue")
    @newspaper_ns.marshal_with(issue_model, envelope = "issue")
    def post(self, paper_id, issue_id):
        issue = Agency.get_instance().release_issue(paper_id, issue_id)
        if not issue:
            newspaper_ns.abort(404, f"Issue with ID {issue_id} was not found")

        return issue
@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor')
class Specify_editor(Resource):

    @newspaper_ns.doc(description = "Specify an editor for an issue")
    @newspaper_ns.expect(specify_editor_model, validate= True )
    def post(self, paper_id, issue_id):
        #take only one editor for an issue
        editor_id = newspaper_ns.payload["editor_id"]
        editor_id_1 = Agency.get_instance().specify_editor(paper_id, issue_id, editor_id)
        if editor_id_1:
            return jsonify(f"The issue was specified this editor {editor_id_1}")
        if not editor_id_1:
            newspaper_ns.abort(404, "Editor, newspaper or issue was not found")
@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/deliver')
class Newspaper_deliver(Resource):
    @newspaper_ns.doc(description = "Send an issue to a subscriber")
    @newspaper_ns.marshal_with(issue_model, envelope="issue")
    def post(self, paper_id, issue_id):

        issue = Agency.get_instance().send_issue_subscriber(paper_id, issue_id)
        if not issue:
            newspaper_ns.abort(404, f"Issue with ID {issue_id} was not found")

        return issue

@newspaper_ns.route('/<int:paper_id>/stats')
class Newspaper_stats(Resource):

    @newspaper_ns.doc(description = "Get the number of newspaper subscriptions and the monthly and annual cost")
    def get(self, paper_id):

        stats = Agency.get_instance().newspaper_stats(paper_id)
        if not stats:
            newspaper_ns.abort(404, f"Newspaper with ID {paper_id} was not found")
        number, price, revenue = stats

        return jsonify(f"Number of subscribers {number}, Monthly price {price} and annual revenue {revenue}")
