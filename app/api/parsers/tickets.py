from flask_restful import reqparse

from app.tickets.models import TicketStatus, TicketResults

ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument('asset_id', type=int, required=True, help='asset_id обязательное поле')
ticket_parser.add_argument('description', type=str, required=True, help='description обязательное поле')
ticket_parser.add_argument('creator_id', type=int, required=True, help='creator_id обязательное поле')
ticket_parser.add_argument('status', type=str, choices=[s.value for s in TicketStatus],
                           default=TicketStatus.OPENED.value)
ticket_parser.add_argument('assignee_id', type=int)
ticket_parser.add_argument('department_id', type=int)
ticket_parser.add_argument('option_id', type=int)

ticket_update_parser = reqparse.RequestParser()
ticket_update_parser.add_argument('status', type=str, choices=[s.value for s in TicketStatus])
ticket_update_parser.add_argument('assignee_id', type=int)
ticket_update_parser.add_argument('department_id', type=int)
ticket_update_parser.add_argument('result', type=str, choices=[r.value for r in TicketResults])
ticket_update_parser.add_argument('option_id', type=int)

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('author_id', type=int, required=True, help='author обязательное поле')
comment_parser.add_argument('text', type=str, required=True, help='text не может быть пустым')
