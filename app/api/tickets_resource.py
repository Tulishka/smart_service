from datetime import datetime

from flask import jsonify

from app import db
from app.api.common import BaseResource, pagination, pagination_response
from app.api.parsers.tickets import ticket_update_parser, comment_parser, ticket_parser
from app.tickets.models import Ticket, TicketStatus, TicketComment, TicketResults


class TicketResource(BaseResource):
    def get(self, ticket_id):
        """Получение заявки по id"""
        ticket = Ticket.query.get_or_404(ticket_id)
        return jsonify(self._ticket_to_dict(ticket))

    def put(self, ticket_id):
        """Обновление заявки"""
        args = ticket_update_parser.parse_args()
        ticket = Ticket.query.get_or_404(ticket_id)

        if 'status' in args:
            args['status'] = TicketStatus(args['status']) if args['status'] else None
        if 'result' in args:
            args['result'] = TicketResults(args['result']) if args['result'] else None

        if args['status'] == TicketStatus.CLOSED and not ticket.is_closed:
            ticket.closed = datetime.now()

        for key, value in args.items():
            if value is not None:
                setattr(ticket, key, value)

        db.session.add(ticket)
        db.session.commit()
        return jsonify(self._ticket_to_dict(ticket))

    def delete(self, ticket_id):
        """Удаление заявки"""
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({'message': 'Заявка удалена'})

    @classmethod
    def _ticket_to_dict(cls, ticket):
        return {
            'id': ticket.id,
            'created': ticket.created.isoformat() if ticket.created else None,
            'asset_id': ticket.asset_id,
            'description': ticket.description,
            'creator_id': ticket.creator_id,
            'status': ticket.status.value,
            'assignee_id': ticket.assignee_id,
            'department_id': ticket.department_id,
            'take_time': ticket.take_time.isoformat() if ticket.take_time else None,
            'closed': ticket.closed.isoformat() if ticket.closed else None,
            'result': ticket.result.value if ticket.result else None,
            'option_id': ticket.option_id,
            'comments': [cls.comment_to_dict(c) for c in ticket.comments]
        }

    @classmethod
    def comment_to_dict(cls, comment):
        return {
            'id': comment.id,
            'author_id': comment.author_id,
            'create': comment.create.isoformat(),
            'text': comment.text
        }


class TicketListResource(BaseResource):
    def get(self):
        """Получение всех заявок"""

        tickets = pagination(Ticket.query)
        return pagination_response(tickets, [TicketResource._ticket_to_dict(t) for t in tickets.items], "tickets")

    def post(self):
        """Создание новой заявки"""
        args = ticket_parser.parse_args()
        args['status'] = TicketStatus(args['status']) if args['status'] else None

        ticket = Ticket(
            asset_id=args['asset_id'],
            description=args['description'],
            creator_id=args['creator_id'],
            status=args['status'],
            result=TicketResults.NEW,
            assignee_id=args.get('assignee_id'),
            department_id=args.get('department_id'),
            option_id=args.get('option_id')
        )

        db.session.add(ticket)
        db.session.commit()
        return jsonify(TicketResource._ticket_to_dict(ticket))


class TicketCommentResource(BaseResource):
    def post(self, ticket_id):
        """Добавление коммента к заявке"""
        args = comment_parser.parse_args()
        ticket = Ticket.query.get_or_404(ticket_id)

        comment = TicketComment(
            author_id=args['author_id'],
            text=args['text'],
            create=datetime.now(),
            ticket_id=ticket.id
        )

        db.session.add(comment)
        db.session.commit()
        return jsonify(TicketResource.comment_to_dict(comment))
