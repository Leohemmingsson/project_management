from ..logging import logger
from ..schemas import NotificationInfo

def send_email(notification_info: NotificationInfo):
    logger.info(f"Sending email to {notification_info.destination}, with template {notification_info.template_id}, with data {notification_info.template_data}")
    ...

    ## If using sendgrid ##

    # from sendgrid import SendGridAPIClient
    # from sendgrid.helpers.mail import Mail, DynamicTemplateData

    # message = Mail(
    #     from_email='you@example.com',
    #     to_emails=mail_to,
    # )
    # message.template_id = template_id
    # message.dynamic_template_data = template_data
    # sg = SendGridAPIClient('your_api_key')
    # sg.send(message)

def send_sms(notification_info: NotificationInfo):
    logger.info(f"Sending sms to {notification_info.destination}, with template {notification_info.template_id}, with data {notification_info.template_data}")
    ...
