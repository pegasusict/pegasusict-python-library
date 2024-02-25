# -*- coding: utf-8 -*-
#  Copyleft  2021-2024 Mattijs Snepvangers.
#  This file is part of Pegasus-ICT Python Library, hereafter named PPL.
#
#  PPL is free software: you can redistribute it and/or modify  it under the terms of the
#   GNU General Public License as published by  the Free Software Foundation, either version 3
#   of the License or any later version.
#
#  PPL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#   without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#   along with PPL.  If not, see <https://www.gnu.org/licenses/>.
import PPL.Exceptions


class Email:

    def send(self, **kwargs):
        import smtplib
        from email.message import EmailMessage
        from email.utils import make_msgid

        host = kwargs.get("host", "mail.pegasus-ict.nl")
        port = kwargs.get("port", 465)
        local_hostname = kwargs.get("local_hostname", None)
        timeout = kwargs.get("timeout", 120)
        context = kwargs.get("context", None)
        source_address = kwargs.get("source_address", None)
        user = kwargs.get("user", None)
        password = kwargs.get("password", None)
        debug = kwargs.get("debug", False)
        sender = kwargs.get("sender", "")
        to = kwargs.get("to", [])
        cc = kwargs.get("cc", [])
        bcc = kwargs.get("bcc", [])
        subject = kwargs.get("subject", "Testing, 1, 2, 3...")
        message_body = kwargs.get("message", "Testing, 1, 2, 3...")
        message_html = kwargs.get("message_html", "<html><body><<h2>Testing, 1, 2, 3...</h2></body></html>")
        attachments: list = kwargs.get("attachments", [])

        mail_options = "SMTPUTF8"

        message = EmailMessage()
        message.set_content(message_body)
        if message_html != '':
            message_id = make_msgid()
            message.add_alternative(message_html.format(message_id=message_id[1:-1]), subtype='html')
        if len(attachments) > 0:
            for attachment in attachments:
                message.add_attachment(attachment)

        message['Subject'] = subject
        message['From'] = sender
        message['To'] = ", ".join(to)
        if cc.count(any) > 0:
            message['Cc'] = ", ".join(cc) or None
        # message['Bcc'] = bcc and ", ".join(bcc) or None

        _smtp_srv = smtplib.SMTP_SSL(host=host, port=port, local_hostname=local_hostname, timeout=timeout, context=context,
                                     source_address=source_address)
        _smtp_srv.login(self, user=user, password=password, initial_response_ok=True)
        if debug:
            _smtp_srv.set_debuglevel(2)
        _smtp_srv.send_message(message, from_addr=sender, to_addrs=(", ".join(to) + ", ".join(cc) + ", ".join(bcc)))
        _smtp_srv.quit()

    def check(self, host: str = '', port=0, user="", password=""):

        imap_ssl_host = host or "localhost"
        imap_ssl_port = port or 993
        if user:
            username = user
        else:
            raise PPL.Exceptions.CommunicationException("Email.check(): No username set")
        if not password:
            raise PPL.Exceptions.CommunicationException("Email.check(): No password set")


