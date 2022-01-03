from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_mail(to: str, subject: str, template: str, **kwargs) -> None:
    """Helper function to send emails
    # TODO -> use Selery workers"""
    app = current_app._get_current_object()
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
