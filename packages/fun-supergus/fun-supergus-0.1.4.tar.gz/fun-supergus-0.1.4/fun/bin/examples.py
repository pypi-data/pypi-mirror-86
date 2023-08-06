"""Examples from the Fun package.

WARNING:
    - You must first configure your SMTP connection. See the method ``_setup_smtp_server()``
      in the Communicator object defined in ``fun/communications/communicator.py``.

"""

import fun

# =================================================================
# Using ET's Communicator...!
# =================================================================

# See the docstring of phone_home() for description of all options.

# Using arbitrary phone numbers or emails:
fun.et.phone_home("Ricki don't lose my number.", 7345555555, subject='Waiting by the phone')
fun.et.phone_home('Howdy, this is my message to you.', '734-555-5555', subject='Message for Chris')
fun.et.phone_home('Have you seen Barney lately?', ['fred@fintstones.com', 'wilma@fintstones.com'], subject='Dinos')

# Using the JSON directory in fun/communications/contact_list.json to target users:
fun.et.phone_home('There can never be too much foo.', 'joe', subject='Foo')

# Using the JSON directory in fun/communications/contact_list.json to target groups:
fun.et.phone_home('Fear is the mindkiller.', ['admin', 'physics'], subject='I must not fear')

# Default is `use_sms=True` and `use_email=False`, but you can change this behavior if you don't
# want people in the directory to receive duplicate emails and SMS messages:
fun.et.phone_home('Need those reports today.', 'physics', subject='TPS Reports', use_email=True, use_sms=False)


# =================================================================
# Using the Fancy Printer...!
# =================================================================

# See the docstring of fancy_print() for description of all options.
fun.fancy_print('I like pretty things', fg='light_pink', bold=True, framed=True)

# Run the built-in demo to see what the printer can do
fun.fancy_print('Foo Fighters Rule', demo=True)

