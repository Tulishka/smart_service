from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', required=True)
user_parser.add_argument("phone", required=True)
user_parser.add_argument("password", required=True)
user_parser.add_argument("department_id", required=False)

user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument('name', required=False)
user_update_parser.add_argument("phone", required=False)
user_update_parser.add_argument("password", required=False)
user_update_parser.add_argument("department_id", required=False)
