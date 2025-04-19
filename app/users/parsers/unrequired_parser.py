from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=False)
parser.add_argument("phone", required=False)
parser.add_argument("password", required=False)
parser.add_argument("department_id", required=False)
