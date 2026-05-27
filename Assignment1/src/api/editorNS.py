from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from ..model.agency import Agency
from ..model.editor import Editor
from .newspaperNS import issue_model
editor_ns = Namespace("editor", description="Editor related operations")

# model for the interface
editor_model = editor_ns.model("EditorModel", {
    "editor_id": fields.Integer(required= False, help = "The unique identifier of a subscriber"),
    "name": fields.String(required = True, help = "The unique identifier of an editor"),
    "address": fields.String(required = True, help = "The address of the editor")
})

@editor_ns.route("/")
class EditorAPI(Resource):

    @editor_ns.doc(editor_model, description = "Add a new editor")
    @editor_ns.expect(editor_model, validate = True)
    @editor_ns.marshal_with(editor_model, envelope = "editor")

    def post(self):


        agency = Agency.get_instance()
        new_editor = Editor(
                            name = editor_ns.payload["name"],
                            address = editor_ns.payload["address"])
        new_editor.editor_id = Agency.next_id(agency.editors, "editor_id")
        new_editor.paper_list = []
        agency.add_editor(new_editor)
        return new_editor

    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def get(self):
        return Agency.get_instance().all_editor()

@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):

    @editor_ns.doc(description="Get a new editor")
    @editor_ns.marshal_with(editor_model, envelope= "editor")
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        if not search_result:
            editor_ns.abort(404, f"Editor with ID {editor_id} was not found")
        return search_result

    @editor_ns.doc(parser = editor_model, description = "Update a new editor")
    @editor_ns.expect(editor_model, validate= True)
    @editor_ns.marshal_with(editor_model, envelope="editor")

    def post(self, editor_id):

        # find the editor by ID
        agency = Agency.get_instance()
        editor = agency.get_editor(editor_id)
        if not editor:
            editor_ns.abort(404, f"Editor with ID {editor_id} was not found")

        updated_editor = Editor( name=editor.name, address=editor.address)
        # update editor data
        updated_editor.name = editor_ns.payload["name"]
        updated_editor.address = editor_ns.payload["address"]
        updated_editor.editor_id = editor_id
        updated_editor.paper_list = editor.paper_list
        agency.update_editor(updated_editor)
        return updated_editor
    @editor_ns.doc(description="Delete a new editor")
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return f"Editor with ID {editor_id} was not found", 404
        Agency.get_instance().remove_editor(targeted_editor)
        return jsonify(f"Editor with ID {editor_id} was removed")


@editor_ns.route('/<int:editor_id>/issues')
class Editorissues(Resource):

    @editor_ns.doc(description="List all newspaper issues")
    @editor_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, editor_id):
        if not Agency.get_instance().get_editor(editor_id):
            editor_ns.abort(404, f"Editor with ID {editor_id} was not found")
        issues = Agency.get_instance().get_list_newspaper_issue_editor(editor_id)

        return issues





