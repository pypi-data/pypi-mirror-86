"""ET Phone Home! Send messages via email and SMS."""

__author__ = "Christopher Couch"
__license__ = "MIT"
__version__ = "2020-11"

import platform
import smtplib
import json
import re
import mimetypes
from string import Template
from pathlib import Path
from email.message import EmailMessage
from email.utils import make_msgid

# Be sure to install fun to your current VENV!
from fun.printing.formatted_console_print import fancy_print


# ==================================================================
# Add your credentials here
# ==================================================================

# To utilize an external email service while outside of a managed network
# Example using Gmail:
# https://support.google.com/mail/answer/7126229?visit_id=637161016079461373-4266744509&hl=en&rd=1
EXTERNAL_HOST = 'smtp.gmail.com'
EXTERNAL_PORT = 587
EXTERNAL_USER_NAME = 'your_email@gmail.com'
EXTERNAL_USER_PWD = 'your_pwd'

# To send an email while inside your company's network
INTERNAL_HOST = 'smtp.your.company.ctb'
INTERNAL_PORT = None
INTERNAL_USER_NAME = 'your_email@your_company.tech'
INTERNAL_USER_PWD = None


# ==================================================================
# Other definitions
# ==================================================================

COMMUNICATOR_MSG_COLOR = 'light_cerulean'
COMMUNICATOR_WARN_COLOR = 'yellow'

root = Path(__file__).parent.absolute()


# ==================================================================
# Main class definition
# ==================================================================

class Communicator(object):
    """Handler for external communications via email and SMS.

    Methods implemented:
        - `send_msg( )` : Sends messages, email and/or SMS.

    """

    def __init__(self):
        """Initial setup."""

        self.attachments_enabled = None
        self.contacts = None
        self.template = None
        self.machine = None
        self.sms_email_stubs = None

        # Can hard-code this later.
        # All outgoing emails will be cc'd to address in this list.
        self.cc_email_list = list()

        self._get_machine_name()
        self._get_contacts(root / 'contact_list.json')
        self._get_template(root / 'email_template.txt')
        self._get_sms_email_stubs(root / 'sms_email_stubs.json')

        return

    def __repr__(self):
        return 'Communications for email and SMS'

    # =====================================================
    # Public methods
    # =====================================================

    def send_msg(self, body, who, subject=None, **kwargs):
        """Sends email and SMS messages.

        **NOTES FOR TARGETING RECIPIENTS WITH 'who':**
            - `'who'` can be a user name, group name, email, or mobile number.
            - It can be an individual item or a list of items.
            - User and group names are defined in ``contact_list.json``.
            - When targeting users or groups, you can toggle the mode of communication using
              `use_email` and `use_sms`. By default, only SMS is used.
            - Mobile numbers can be any format, but they must contain 10 digits in addition to any
              leading 0s or 1s. Integers and strings are OK.

        Arguments:
            body (str): Contents of message.
            who (obj): User name, group name, email, or mobile number. Single items, or a list of many.
                See notes.
            subject (str): Optional. Subject of message. Default is None.

        Keyword Arguments:
            attachment (Path): Path-like object that points to a file.
                Default is None.
            disable_email (bool): If True, emails will not be sent to any recipients.
                This can be useful if you want to send only SMS messages to users or groups in the
                contact_list.json.
                Default is False.
            disable_sms (bool): If True, SMS messages will not be sent to any recipients.
                This can be useful if you want to send only email messages to users or groups in the
                contact_list.json.
                Default is False.

        Returns:
            No returns.
        """

        # ============================================================
        # Parse and bail out if needed
        # ============================================================

        self._parse_who(who)

        if not self._ensure_recipients_exist():
            return

        # Kwargs
        attachment = kwargs.get('attachment', None)
        disable_email = kwargs.get('disable_email', False)
        disable_sms = kwargs.get('disable_sms', False)

        if not self._ensure_attachment_exists(attachment):
            return

        for b, n in zip([disable_email, disable_sms], ['disable_email', 'disable_sms']):
            if not isinstance(b, bool):
                msg = f'\'{n}\' must be boolean but you gave type {type(b)}'
                raise TypeError(msg)

        # ============================================================
        # Main
        # ============================================================

        with self._setup_smtp_server() as sess:

            # Create msg object
            msg = EmailMessage()

            # Personalize the template
            body_from_template = self.template.substitute(BODY=body)

            # Set msg parameters;
            # Note we will assign msg['To'] below when iterating over email addresses
            msg['From'] = self.sender_address
            msg['Subject'] = subject.upper() if isinstance(subject, str) else None

            # Copy outgoing emails to cc list
            if isinstance(self.cc_email_list, list):
                if len(self.cc_email_list) > 0:
                    msg['CC'] = ','.join(self.cc_email_list)

            # Base text message
            msg.set_content(body_from_template)

            # HTML version
            body_html = re.sub(r'[\n]', '<br>', body_from_template)  # Replace /n with <br>
            logo_cid = make_msgid()
            msg.add_alternative("""\
            <html>
              <head></head>
              <body>
                <p>""" + body_html + '</p>' + """
                <a href="https://www.liveline.tech">
                <img src="cid:{logo_cid}" />
                </a>
              </body>
            </html>
            """.format(logo_cid=logo_cid[1:-1]), subtype='html')

            # Add logo to the HTML version
            t = root / 'liveline_logo.png'
            with open(t, 'rb') as img:
                r = img.read()
                # noinspection PyUnresolvedReferences
                msg.get_payload()[1].add_related(r, 'image', 'png', cid=logo_cid)

            # Optionally attach a file
            # First use mimetypes to try and guess content type based on file extension:
            if attachment is not None:
                attachment = Path(attachment)
                ctype, encoding = mimetypes.guess_type(str(attachment))
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                maintype += f'; name="{attachment.name}"'
                with open(attachment, 'rb') as file:
                    r = file.read()
                    msg.add_attachment(r, maintype=maintype, subtype=subtype)

            # ============================================================
            # Email
            # ============================================================

            # For each email & phone in current lists, send messages
            if not disable_email:
                for e in self.current_email_list:

                    # Console out
                    stdout_msg = f'COMMUNICATOR MESSAGE: Sending email to: '
                    fancy_print(stdout_msg, fg=COMMUNICATOR_MSG_COLOR, end='')
                    fancy_print(e, fg='hlink')

                    # Update msg 'To:' field
                    if msg['To'] is not None:
                        del msg['To']
                    msg['To'] = e

                    # # Make a local copy of what we are going to send... to a log file?
                    # with open('outgoing.msg', 'wb') as f:
                    #     f.write(bytes(msg))

                    try:
                        sess.send_message(msg)
                    except:
                        stdout_msg = f'COMMUNICATOR WARNING: Failed sending email message'
                        fancy_print(stdout_msg, fg=COMMUNICATOR_WARN_COLOR)

            # ============================================================
            # SMS
            # ============================================================

            if not disable_sms:
                for m in self.current_mobile_list:

                    # Console out
                    stdout_msg = f'COMMUNICATOR MESSAGE: Sending SMS message to: '
                    fancy_print(stdout_msg, fg=COMMUNICATOR_MSG_COLOR, end='')
                    fancy_print(m[0:3] + '.' + m[3:6] + '.' + m[6:10], fg='cerulean')

                    any_ok = False
                    candidates = list()

                    # Try all the stubs!
                    # We don't know the carrier name.
                    # Assume the invalid addresses will get black-holed by the various carriers.
                    for stub in self.sms_email_stubs:
                        candidates.append(m + self.sms_email_stubs[stub])

                    # Update msg 'To:' field
                    if msg['To'] is not None:
                        del msg['To']
                    msg['To'] = candidates

                    # # Make a local copy of what we are going to send... to a log file?
                    # with open('outgoing.msg', 'wb') as f:
                    #     f.write(bytes(msg))

                    try:
                        sess.send_message(msg)
                        any_ok = True
                    except:
                        pass

                    if not any_ok:
                        stdout_msg = f'COMMUNICATOR WARNING: Failed sending SMS message'
                        fancy_print(stdout_msg, fg=COMMUNICATOR_WARN_COLOR)

        return

    # =====================================================
    # Private methods
    # =====================================================

    def _get_machine_name(self):
        """Returns machine name and stores in state attribute."""
        self.machine = platform.uname().node
        return self.machine

    def _setup_smtp_server(self):
        """Returns an smtp server object."""

        # Init; Attempt to use external first
        target = 'external'

        # ============================================================
        # Attempt (1): External mail server
        # ============================================================

        if target == 'external':
            # Assume it's a machine external to company network.
            # We will use an external email account that requires a login.

            # msg = f'_setup_smtp_server(): Attempting to launch session as external machine...'
            # fancy_print(msg, fg=COMMUNICATOR_MSG_COLOR, bold=True)

            self.host = EXTERNAL_HOST
            self.port = EXTERNAL_PORT
            self.sender_address = EXTERNAL_USER_NAME
            self.sender_pwd = EXTERNAL_USER_PWD

            try:
                sess = smtplib.SMTP(host=self.host, port=self.port)
                sess.starttls()
                sess.login(self.sender_address, self.sender_pwd)
                return sess
            except:
                target = 'internal'

        # ============================================================
        # Attempt (2): Company internal mail server
        # ============================================================

        if target == 'internal':
            # Assume machine is internal to company network.
            # Current user should already be authenticated.

            # msg = f'_setup_smtp_server(): Attempting to launch session as internal Cooper machine...'
            # fancy_print(msg, fg=COMMUNICATOR_MSG_COLOR, bold=True)

            self.host = INTERNAL_HOST
            self.port = INTERNAL_PORT
            self.sender_address = INTERNAL_USER_NAME
            self.sender_pwd = INTERNAL_USER_PWD

            try:
                sess = smtplib.SMTP(self.host)
                return sess
            except:
                msg = f'COMMUNICATOR WARNING: Could not establish SMTP connection. Check configuration.'
                fancy_print(msg, fg=COMMUNICATOR_WARN_COLOR)

        msg = f'Could not establish SMTP connection'
        raise ConnectionError(msg)

    def _get_contacts(self, tgt):
        """Reads contact information from a JSON contact file.

        Assigns to ``self.communications``: A nested dict with top-level keys 'groups', 'users'.

        Arguments:
            tgt (str): A valid path and filename for the JSON contact list.
        """
        with open(tgt, mode='r', encoding='utf-8') as f:
            str_contents = f.read()
        self.contacts = json.loads(str_contents)
        return

    def _get_template(self, tgt):
        """Returns a Python string template for use in messages.

        Assigns to ``self.template``: A Python string template.

        Arguments:
            tgt (str): A valid path and filename for the template text file.
        """
        with open(tgt, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        self.template = Template(template_file_content)
        return

    def _get_sms_email_stubs(self, tgt):
        """Reads SMS email stub info from a JSON file.

        Assigns to ``self.sms_email_stubs``: A dict.

        Arguments:
            tgt (str): A valid path and filename for the JSON file.
        """
        with open(tgt, mode='r', encoding='utf-8') as f:
            str_contents = f.read()
        self.sms_email_stubs = json.loads(str_contents)
        return

    def _parse_who(self, who):
        """Parses who argument from send_msg().

        **ALLOWABLE VALUES FOR 'who':**
            - User name in self.communications.users
            - Group name in self.communications.group
            - Arbitrary mobile number (any format); one string or 10-digit integer, or a list of strings/integers.
            - Arbitrary email address; one string or a list of strings
            - 'who' will be parsed in that order, and the first "hit" wins.

        """

        if not (isinstance(who, str) or isinstance(who, list) or isinstance(who, int)):
            msg = f'\'who\' must be a string or list but you gave type {type(who)}'
            raise TypeError(msg)

        if self.contacts is None:
            self._get_contacts(root / 'contact_list.json')
            if self.contacts is None:
                msg = f'No communications available in self.communications after calling self._get_contacts()'
                raise RuntimeError(msg)

        users = self.contacts['users']
        groups = self.contacts['groups']
        self.current_email_list = None
        self.current_mobile_list = None

        # NOTE: If who is in BOTH 'users' and 'groups', the contact info in 'users' will be used.

        # Ensure who is a list
        if not isinstance(who, list):
            who = [who]

        # Iterate over list elements and parse
        final_email_list = list()
        final_mobile_list = list()

        for w in who:

            w_email_list, w_mobile_list = list(), list()
            got_a_mobile, got_an_email, hit = False, False, False

            # Case 1: 'who' is a 'user'
            if w in users:

                # Extract from communications
                w_email_list = [users[w]['email'] if 'email' in users[w] else None]
                w_mobile_list = [users[w]['mobile'] if 'mobile' in users[w] else None]

                # Cleanse the emails (contents in communications may not be kosher)
                valid_emails, got_an_email = self._cleanse_emails(w_email_list)
                if got_an_email:
                    hit = True
                    for elem in valid_emails:
                        final_email_list.append(elem)

                # Cleanse the mobiles (contents in communications may not be kosher)
                valid_mobiles, got_a_mobile = self._cleanse_phone_numbers(w_mobile_list)
                if got_a_mobile:
                    hit = True
                    for elem in valid_mobiles:
                        final_mobile_list.append(elem)

            # Case 2: 'who' is a group of users in 'group'
            if w in groups and not hit:

                # Extract from communications
                user_list = groups[w]
                w_email_list = list()
                w_mobile_list = list()
                for u in user_list:
                    e = users[u]['email'] if 'email' in users[u] else None
                    m = users[u]['mobile'] if 'mobile' in users[u] else None
                    w_email_list.append(e)
                    w_mobile_list.append(m)

                # Cleanse the emails (contents in communications may not be kosher)
                valid_emails, got_an_email = self._cleanse_emails(w_email_list)
                if got_an_email:
                    hit = True
                    for elem in valid_emails:
                        final_email_list.append(elem)

                # Cleanse the mobiles (contents in communications may not be kosher)
                valid_mobiles, got_a_mobile = self._cleanse_phone_numbers(w_mobile_list)
                if got_a_mobile:
                    hit = True
                    for elem in valid_mobiles:
                        final_mobile_list.append(elem)

            # Case 3: 'w' is an arbitrary phone number
            if not hit:

                # Cleanse the mobiles
                valid_mobiles, got_a_mobile = self._cleanse_phone_numbers(w)
                if got_a_mobile:
                    hit = True
                    for elem in valid_mobiles:
                        final_mobile_list.append(elem)

            # Case 4: 'w' is an arbitrary email address
            if not hit:

                # Cleanse the emails
                valid_emails, got_an_email = self._cleanse_emails(w)
                if got_an_email:
                    hit = True
                    for elem in valid_emails:
                        final_email_list.append(elem)

        # Final assignments, no duplicates
        self.current_mobile_list = list(set(final_mobile_list))
        self.current_mobile_list.sort()
        self.current_email_list = list(set(final_email_list))
        self.current_email_list.sort()

        return

    def _ensure_recipients_exist(self):
        if len(self.current_mobile_list) == 0 and len(self.current_email_list) == 0:
            msg = f'COMMUNICATOR WARNING: No recipients identified. Check for valid phone/mobile.'
            fancy_print(msg, fg=COMMUNICATOR_WARN_COLOR)
            return False
        else:
            return True

    @staticmethod
    def _cleanse_phone_numbers(numbers):
        """Returns a list containing strings of 10 digits or None,
        and a Boolean flag denoting whether we have at least one valid number."""

        hit = False

        # Ensure we have a list.
        # Might have received a single string or long integer.
        if not isinstance(numbers, list):
            numbers = [numbers]

        cleansed_list = list()

        for i, elem in enumerate(numbers):

            # Only append if it's a valid email
            if elem is not None:

                # Convert integers (and others) to string
                wip = str(elem)

                # Isolate decimal numbers
                wip = ''.join(e for e in wip if e.isdecimal())

                # Strip leading 0 and 1s, if there was more than one decimal number
                if len(wip) > 1:
                    while wip[0] in ['0', '1'] and len(wip) > 1:
                        wip = wip[1:]

                # Append IFF we have a string with 10 digits
                if len(wip) == 10:
                    cleansed_list.append(wip)
                    hit = True

            else:
                pass

        # Handle case: No valid number-strings in the list
        cleansed_list = [None] if len(cleansed_list) == 0 else cleansed_list

        return cleansed_list, hit

    @staticmethod
    def _cleanse_emails(emails):
        """Returns a list containing strings of emails or None,
        and a Boolean flag denoting whether we have at least one valid email."""

        hit = False

        # Ensure we have a list.
        # Might have received a single string.
        if not isinstance(emails, list):
            emails = [emails]

        cleansed_list = list()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,5}$'

        # Alternative:
        # regex_valid_email = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,5})+$')
        # is_email = True if regex_valid_email.match(contact_method) else False

        for i, elem in enumerate(emails):

            # Only append if it's a valid email
            if elem is not None:
                if re.search(regex, elem):
                    cleansed_list.append(elem)
                    hit = True

        # Handle case: No valid emails in the list
        cleansed_list = [None] if len(cleansed_list) == 0 else cleansed_list

        return cleansed_list, hit

    @staticmethod
    def _ensure_attachment_exists(target):
        """Returns True if the targeted path exists (or is None) and false otherwise."""
        if target is not None:
            target = Path(target)
            if not target.exists():
                msg = f'COMMUNICATOR WARNING: The file specified for attachment to email does not exist'
                fancy_print(msg, fg=COMMUNICATOR_WARN_COLOR)
                return False
        return True


# ==================================================================
# Public function - utilizes the Communicator class
# ==================================================================

def phone_home(body, who, subject=None, **kwargs):
    """Sends email and SMS messages.

    **NOTES FOR TARGETING RECIPIENTS WITH 'who':**
        - `'who'` can be a user name, group name, email, or mobile number.
        - It can be an individual item or a list of items.
        - User and group names are defined in ``contact_list.json``.
        - When targeting users or groups, you can toggle the mode of communication using
          `use_email` and `use_sms`. By default, only SMS is used.
        - Mobile numbers can be any format, but they must contain 10 digits in addition to any
          leading 0s or 1s. Integers and strings are OK.

    Arguments:
        body (str): Contents of message.
        who (obj): User name, group name, email, or mobile number. Single items, or a list of many.
            See notes.
        subject (str): Optional. Subject of message. Default is None.

    Keyword Arguments:
        attachment (Path): Path-like object that points to a file.
            Default is None.
        disable_email (bool): If True, emails will not be sent to any recipients.
            This can be useful if you want to send only SMS messages to users or groups in the
            contact_list.json.
            Default is False.
        disable_sms (bool): If True, SMS messages will not be sent to any recipients.
            This can be useful if you want to send only email messages to users or groups in the
            contact_list.json.
            Default is False.

    Returns:
        No returns.
    """
    c = Communicator()
    c.send_msg(body, who, subject, **kwargs)






