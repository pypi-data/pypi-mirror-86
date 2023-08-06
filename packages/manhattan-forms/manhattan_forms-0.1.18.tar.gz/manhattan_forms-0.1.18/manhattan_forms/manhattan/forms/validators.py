import re
import string
from urllib.parse import urlparse

import email_validator
import flask
from mongoframes import And, Q
import phonenumbers
import wtforms.validators
from wtforms.validators import *
from wtforms.validators import ValidationError

# WTForm validators are passed through to provide a single access point
__all__ = set(wtforms.validators.__all__)
__all__.add('Email')
__all__.add('ErrorMessage')
__all__.add('Password')
__all__.add('PathOrURL')
__all__.add('PhoneNumber')
__all__.add('PseudoRequired')
__all__.add('RequiredIf')
__all__.add('ValidationError')
__all__.add('UniqueDocument')
__all__ = tuple(__all__)


class Email:
    """
    WTForms has resolved a number of issues with email validation, however,
    the update is not yet available in a release and so as a temporary short
    term fix we've added the new validator into manhattan-forms.
    """

    def __init__(
        self,
        message=None,
        granular_message=False,
        check_deliverability=False,
        allow_smtputf8=True,
        allow_empty_local=False,
    ):
        self.message = message
        self.granular_message = granular_message
        self.check_deliverability = check_deliverability
        self.allow_smtputf8 = allow_smtputf8
        self.allow_empty_local = allow_empty_local

    def __call__(self, form, field):
        try:
            if field.data is None:
                raise email_validator.EmailNotValidError()

            email_validator.validate_email(
                field.data,
                check_deliverability=self.check_deliverability,
                allow_smtputf8=self.allow_smtputf8,
                allow_empty_local=self.allow_empty_local,
            )

        except email_validator.EmailNotValidError as e:
            message = self.message
            if message is None:
                if self.granular_message:
                    message = field.gettext(e)
                else:
                    message = field.gettext('Invalid email address.')
            raise wtforms.validators.ValidationError(message)


class ErrorMessage(str):
    """
    The `ErrorMessage` class allows additional error information to be included
    with an error message. This can be useful when validators have additional
    information to relay to the user such as a suggested alternative to an
    invalid value.
    """

    def __new__(cls, content, raised_by, **kwargs):

        # The object that raised the error
        cls.raised_by = raised_by

        # Additional error information is add based on the kwargs
        for k, v in kwargs.items():
            setattr(cls, k, v)

        return str.__new__(cls, content)


class Password:
    """
    Validate that a password meets a given critera to be consider 'safe'.

    Whilst the validator can't ensure a password is 'save' it provides a way
    to implement common rules required by organizations for passwords.
    """

    def __init__(
        self,
        min_length=8,
        max_length=256,
        min_lower=1,
        min_upper=1,
        min_digits=1,
        min_specials=1
    ):

        self.min_length = min_length
        self.max_length = max_length
        self.min_upper = min_upper
        self.min_lower = min_lower
        self.min_digits = min_digits
        self.min_specials = min_specials

    def __call__(self, form, field):

        password = field.data
        if not password:
            return

        # Validate the length (min, max)
        if self.min_length:
            if len(password) < self.min_length:
                raise ValidationError(
                    'Min. password length is {0}.'.format(self.min_length)
                )

        if self.max_length:
            if len(password) > self.max_length:
                raise ValidationError(
                    'Max. password length is {0}.'.format(self.max_length)
                )

        # Validate lowercase character requirements
        if self.min_lower:
            lower_len = len([
                c for c in password if c in string.ascii_lowercase
            ])
            if lower_len < self.min_lower:
                raise ValidationError(
                    (
                        'Passwords require at least {0} '
                        'lowercase character{1}.'
                    ).format(
                        self.min_lower,
                        '' if self.min_lower == 1 else 's'
                    )
                )

        # Validate uppercase character requirements
        if self.min_upper:
            upper_len = len([
                c for c in password if c in string.ascii_uppercase
            ])
            if upper_len < self.min_upper:
                raise ValidationError(
                    (
                        'Passwords require at least {0} '
                        'uppercase character{1}.'
                    ).format(
                        self.min_upper,
                        '' if self.min_upper == 1 else 's'
                    )
                )

        # Validate the digit requirements
        if self.min_digits:
            digits_len = len([
                c for c in password if c in string.digits
            ])
            if digits_len < self.min_digits:
                raise ValidationError(
                    'Passwords require at least {0} digit{1}.'.format(
                        self.min_digits,
                        '' if self.min_digits == 1 else 's'
                    )
                )

        # Validate specials
        if self.min_specials:
            non_specials = string.ascii_letters + string.digits
            specials_len = len([
                c for c in password if c not in non_specials
            ])
            if specials_len < self.min_specials:
                raise ValidationError(
                    (
                        'Passwords require at least {0} special '
                        '(non-alphanumeric) character{1}.'
                    ).format(
                        self.min_specials,
                        '' if self.min_specials == 1 else 's'
                    )
                )


class PathOrURL:
    """
    Validate that a field's value is a valid path (/some-path) or URL.
    """

    def __init__(self, message=None):
        self.message = message or 'This is not a valid path or URL.'

    def __call__(self, form, field):

        err = ValidationError(field.gettext(self.message))

        try:
            result = urlparse(field.data)

            if result.scheme and result.netloc:
                return

            if result.path and field.data.startswith('/'):
                return

            raise err

        except ValueError:
            raise err

class PhoneNumber:
    """
    Validate a phone number.
    """

    def __init__(
        self,
        message=None,
        region=None
    ):
        self.message = message

        # The region to validate the number for
        self.region = region

    def __call__(self, form, field):
        if not field.data:
            return

        try:
            number = phonenumbers.parse(field.data, self.region)
            if not phonenumbers.is_valid_number(number):
                raise ValidationError('Not a valid phone number.')

        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError('Not a valid phone number.')


class PseudoRequired:
    """
    The `PseudoRequired` validator is used when you need a field to appear
    required even though the field itself isn't. This is a common requirement
    for tokenizer fields.
    """

    field_flags = ('required',)

    def __call__(self, form, field):
        return


class RequiredIf:
    """
    The `RequiredIf` validator allows the parent field to be flagged as required
    only if certain conditions are met.

    The set of conditions are specified using keywords when initializing the
    validator, for example:

        send_by = SelectField(
            'Send by',
            choices=[('sms', 'SMS'), ('email', 'Email')]
            )
        email = StringField('Email', [RequiredIf(send_by='email')])
        mobile_no = StringField('Mobile no.', [RequiredIf(send_by='sms')])
    """

    def __init__(self, **conditions):
        self.conditions = conditions

    def __call__(self, form, field):
        for name, value in self.conditions.items():

            assert name in form._fields, \
                'Condition field does not present in form.'

            # Check if the condition is met
            if form._fields.get(name).data == value:
                return InputRequired()(form, field)

        Optional()(form, field)


class UniqueDocument:
    """
    Validate that a field value is unique within a set of documents (optionally
    the set can be filtered).

    If a field value is found not to be unique and endpoint/args arguments are
    provided then the error raised will include a link to the view the other
    document with the same value.
    """

    def __init__(self, frame_cls, case_sensitive=True, endpoint=None,
                endpoint_args=None, alternative=None, message=None,
                collation=None, **kwargs):

        # The frame class representing the document set
        self.frame_cls = frame_cls

        # A filter (either a query or function that returns a query) used to
        # filter the set of documents that must be unique.
        if 'filter' in kwargs:
            self.filter = kwargs['filter']
        else:
            self.filter = self.__class__.default_filter

        # A flag indicating if the unqiue nature of the field's value is case
        # sensitive.
        self.case_sensitive = case_sensitive

        # The collation to use when searching a duplicate document
        self.collation = collation

        # An endpoint and arguments that can be used to build a link to another
        # document with the same value. The end point arguments can either be a
        # dictionary or a function.
        self.endpoint = endpoint
        self.endpoint_args = endpoint_args

        # If alternative is specified it must be callable object that accepts
        # a value and an attempt index and returns an alternative value that
        # may be unique, e.g:
        #
        #     lambda v, i: '{v}-{i}'.format(v, i + 1)
        #
        # Would return the following for the string `my-example`:
        #
        #     > 'my-example-1'
        #     > 'my-example-2'
        #     > 'my-example-3'
        #
        # And so on. The field will try at most 100 times to generate a valid
        # unique alternative value before giving up.
        self.alternative = alternative

        # The error message to display if the asset isn't the required type
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            return

        # Build the filter for the set of documents that must be unique
        base_filter = None
        if callable(self.filter):
            base_filter = self.filter(form, field)
        elif self.filter:
            base_filter = self.filter

        # Check the document is unique
        value = field.data
        other = self.find_matching(field.name, value, base_filter)
        if other:

            # If an endpoint is defined build a link to the other document
            url = None
            if self.endpoint:
                kwargs = self.endpoint_args
                if callable(self.endpoint_args):
                    kwargs = self.endpoint_args(other)
                url = flask.url_for(self.endpoint, **kwargs)

            # If an alternative callable is defined attempt to find a valid
            # alternative.
            alternative = None
            if self.alternative:
                for i in range(0, 100):
                    new_value = self.alternative(value, i)
                    if self.is_unique(field.name, new_value, base_filter):
                        alternative = new_value
                        break

            # Compile the message for the error
            message = self.message
            mark_safe = True
            if message is None:
                message = field.gettext(
                    'Another document exists with the same value.')

            message = ErrorMessage(
                message,
                self,
                alternative=alternative,
                matching_url=url
                )

            # Raise a validation error
            raise ValidationError(message)

    def find_matching(self, name, value, base_filter):
        """Return any document that matches the given value"""

        if not self.case_sensitive:
            value = re.compile('^' + re.escape(value) + '$', re.I)
        filter = Q[name] == value

        if base_filter:
            filter = And(filter, base_filter)
        return self.frame_cls.one(filter, collation=self.collation)

    def is_unique(self, name, value, base_filter):
        """Return True if the given value is unique"""

        if not self.case_sensitive:
            value = re.compile(value, re.I)
        filter = Q[name] == value

        if base_filter:
            filter = And(filter, base_filter)
        return self.frame_cls.count(filter, collation=self.collation) == 0

    @staticmethod
    def default_filter(form, field):
        """
        The default filter applied when checking if a field is unique, by
        default we return a filter that checks if a document is being updated
        and if so excludes itself from the unique test.
        """
        if form.obj:
            return Q._id != form.obj._id
