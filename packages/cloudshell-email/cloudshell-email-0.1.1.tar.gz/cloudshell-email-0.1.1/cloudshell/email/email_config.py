from typing import Dict


class EmailConfig:
    def __init__(self, smtp_server: str, user: str, password: str, from_address: str, smtp_port=587,
                 default_subject: str = '', default_html: str = '', default_parameters: Dict[str, str] = {}):
        """
        :param smtp_server:
        :param user: must in an email_service address format
        :param password: password for user email_service address
        :param from_address: the address to be used as the sender
        :param smtp_port:
        """
        self.smtp_server = smtp_server
        self.user = user
        self.password = password
        self.from_address = from_address
        self.smtp_port = smtp_port
        self.default_subject = default_subject
        self.default_html = default_html
        self.default_parameters = default_parameters