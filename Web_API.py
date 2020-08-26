from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

Task_Status = {1: {
    "link": None,
    "ref": None,
    "task state": None, # scheduled, started or completed
    "task status": None, # idle, in progress or completed
    "request_time": None,
    "end_time": None,
    "Owner": None
}
}

BASE = "http://127.0.0.1:5000/" # Our base URI

next_task_id = 0


def generate_id():
    global next_task_id
    this_task = next_task_id
    next_task_id += 1
    return this_task


new_search_args = reqparse.RequestParser()
new_search_args.add_argument("search_area", type=str)
new_search_args.add_argument("max_bedrooms", type=int)
new_search_args.add_argument("min_bedrooms", type=int)
new_search_args.add_argument("max_price", type=int)
new_search_args.add_argument("min_price", type=int)
new_search_args.add_argument("show_bungalow", type=bool)
new_search_args.add_argument("show_detached", type=bool)
new_search_args.add_argument("show_semi-detached", type=bool)
new_search_args.add_argument("show_terraced", type=bool)
new_search_args.add_argument("show_flat", type=bool)
new_search_args.add_argument("show_land", type=bool)
new_search_args.add_argument("must_have_garden", type=bool)
new_search_args.add_argument("must_have_parking", type=bool)
new_search_args.add_argument("dont_show_new-home", type=bool)
new_search_args.add_argument("dont_show_retirement", type=bool)
new_search_args.add_argument("dont_show_shared-ownership", type=bool)


class NewSearch(Resource):
    def put(self):
        args = new_search_args.parse_args()
        search_id = generate_id()
        search_accepted = {}
        search_accepted["ID"] = search_id
        search_accepted["URI"] = BASE + "pending/" + str(search_id)
        return search_accepted, 202


class CheckStatus(Resource):
    def get(self, search_id):
        return {search_id:"Status Checked!"}


class ReturnResults(Resource):
    def get(self, search_id):
        return {search_id: "Here's where the results would be"}


api.add_resource(NewSearch, "/")
api.add_resource(CheckStatus, "/pending/<int:search_id>")
api.add_resource(ReturnResults, "/completed/<int:search_id>")

if __name__ == '__main__':
    app.run(debug=True)
