from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from Scraper_Class import RightMoveScrapper

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


object_dictionary = {}

new_search_args = reqparse.RequestParser()
new_search_args.add_argument("search_area", type=str)
new_search_args.add_argument("max_bedrooms", type=int)
new_search_args.add_argument("min_bedrooms", type=int)
new_search_args.add_argument("max_price", type=int)
new_search_args.add_argument("min_price", type=int)
new_search_args.add_argument("show_house_type", action="append")
new_search_args.add_argument("must_have", action="append")
new_search_args.add_argument("dont_show", action="append")


class NewSearch(Resource):
    def put(self):
        args = new_search_args.parse_args()
        search_id = generate_id()
        search_accepted = {"ID": search_id, "URI": BASE + "pending/" + str(search_id)}
        rightmove_scraper = RightMoveScrapper(**args)
        results = rightmove_scraper.scrape()
        print(results)
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
