from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from .newspaperNS import issue_model #needed to find all undelivered issues
from ..model.agency import Agency
from ..model.subscriber import Subscriber

subscriber_ns = Namespace("subscriber", description="Subscriber related operations")

subscriber_model = subscriber_ns.model("SubscriberModel", {
    "subscriber_id": fields.Integer(required= False, help = "The unique identifier of a subscriber"),
    "name": fields.String(required = True, help ="The name of the subscriber"),
    "address": fields.String(required = True, help = "The address of the subscriber")
})

subscribe_subscriber_model = subscriber_ns.model("Subscribe_subscriber",
{"paper_id": fields.Integer(required = False, help = "The unique identifier of a newspaper")
 })

subscribe_special_issue = subscriber_ns.model("Subscribe_special_issue", {
    "paper_id": fields.Integer(required = False, help = "The unique identifier of a subscriber"),
    "issue_id": fields.Integer(required = False, help = "The unique identifier of an issue")
})


@subscriber_ns.route("/")
class SubscriberAPI(Resource):

    @subscriber_ns.doc(subscriber_model, description="Add a new subscriber")
    @subscriber_ns.expect(subscriber_model, validate = True)
    @subscriber_ns.marshal_with(subscriber_model, envelope = "subscriber")
    def post(self):



        agency = Agency.get_instance()
        new_subscriber=Subscriber(
                              name=subscriber_ns.payload['name'],
                              address=subscriber_ns.payload['address'])
        new_subscriber.subscriber_id = Agency.next_id(agency.subscribers, "subscriber_id")
        new_subscriber.newspaper_list = []
        new_subscriber.specialissue_list = []
        agency.add_subscriber(new_subscriber)
        #create a new subscriber object and add it

        return new_subscriber #return the new subscriber in order to see the added subscriber in the interface

    @subscriber_ns.marshal_list_with(subscriber_model, envelope='subscriber')
    def get(self):
        return Agency.get_instance().all_subscriber() #returns all subscriber in Json


@subscriber_ns.route('/<int:subscriber_id>')
class SubscriberID(Resource):

    @subscriber_ns.doc(description="Get a new subscriber")
    @subscriber_ns.marshal_with(subscriber_model, envelope="subscriber")
    def get(self, subscriber_id):
        search_result = Agency.get_instance().get_subscriber(subscriber_id)
        if not search_result:
            subscriber_ns.abort(404, f"Subscriber with ID {subscriber_id} was not found")
        return search_result

    @subscriber_ns.doc(parser= subscriber_model, description="Update a new subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope="subscriber")

    def post (self, subscriber_id):
        # find the subscriber by ID
        agency = Agency.get_instance()
        subscriber = agency.get_subscriber(subscriber_id)
        if not subscriber:
            subscriber_ns.abort(404, f"Subscriber with ID {subscriber_id} was not found")

        updated_subscriber = Subscriber(name=subscriber.name, address=subscriber.address)

        #update subscriber data
        updated_subscriber.name = subscriber_ns.payload["name"]
        updated_subscriber.address = subscriber_ns.payload["address"]
        updated_subscriber.subscriber_id = subscriber_id
        updated_subscriber.newspaper_list = subscriber.newspaper_list
        updated_subscriber.specialissue_list = subscriber.specialissue_list
        agency.update_subscriber(updated_subscriber)
        return updated_subscriber

    @subscriber_ns.doc(description="Delete a new subscriber")
    #When a client is removed (e.g., cancels a subscription), all subscriptions are stopped
    # The way I understood the assignment was to delete the subscriber and remove the newspapaer subscription which is automitically if I remove the subscriber because the list is an attribute of an subscriber
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return f"Subscriber with ID {subscriber_id} was not found", 404
        Agency.get_instance().remove_subscriber(targeted_subscriber)
        return jsonify(f"Subscriber with ID {subscriber_id} was removed") # In my opinion a statement if the subscriber was removed is enogh

@subscriber_ns.route('/<int:subscriber_id>/subscribe')
class Subscribe_newspaper(Resource):
    #create a model to use the paper_id
    # use payload to use the paper_id
    @subscriber_ns.doc(description = "Subscribe a subscriber to a newspaper")
    @subscriber_ns.expect(subscribe_subscriber_model, validate = True)
    def post(self, subscriber_id):
        paper_id = subscriber_ns.payload["paper_id"]
        paper_id_returned = Agency.get_instance().subscribe_newspaper(subscriber_id, paper_id)

        if paper_id_returned:
            return jsonify(f"The subscriber subscribed this newspaper {paper_id_returned}") # Instead of returning a model a sentence gives more clarity
        if not paper_id_returned:
            return f"Subscriber with ID {subscriber_id} or newspaper with ID {paper_id} was not found", 404

@subscriber_ns.route('/<int:subscriber_id>/subscribe/special_issue')
class Subscribe_special_issue(Resource):
    @subscriber_ns.doc(description = "Subscribe a special issue")
    @subscriber_ns.expect(subscribe_special_issue, validate = True)
    def post(self, subscriber_id):
        paper_id = subscriber_ns.payload["paper_id"]
        issue_id = subscriber_ns.payload["issue_id"]
        issue_id_returned = Agency.get_instance().subscribe_special_issue(subscriber_id, paper_id, issue_id)

        if issue_id_returned:
            return jsonify(f"The subscriber subscribed this issue {issue_id_returned}")
        if not issue_id_returned:
            return "Subscriber, newspaper or issue was not found", 404
@subscriber_ns.route('/<int:subscriber_id>/stats')
class Subscriberstats(Resource):

    @subscriber_ns.doc(description = "Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper.")
    def get(self, subscriber_id):

        stats = Agency.get_instance().subscriber_stats(subscriber_id)
        if not stats:
            subscriber_ns.abort(404, f"Subscriber with ID {subscriber_id} was not found")
        price, annual_cost, delivered_issues, newspaper_number = stats

        return jsonify(f"The number of newspapers subscriptions is {newspaper_number}."
                       f"The monthly and annual cost is {price} and {annual_cost}."
                       f"The number of issues the subscriber received {delivered_issues}.")


@subscriber_ns.route('/<int:subscriber_id>/missingissues')
class Check_undelivered_issues(Resource):

    @subscriber_ns.doc(description = "Check undelivered issues")
    @subscriber_ns.marshal_list_with(issue_model, envelope = "issues")
    def get(self, subscriber_id):

        undelivered_issues = Agency.get_instance().check_undelivered_issues(subscriber_id)
        if undelivered_issues is None:
            subscriber_ns.abort(404, f"Subscriber with ID {subscriber_id} was not found")

        return undelivered_issues
