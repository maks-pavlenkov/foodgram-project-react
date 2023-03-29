from django.core.validators import RegexValidator


regex_tag_color = RegexValidator(
        r'^#(?:[0-9a-fA-F]{1,2}){3}$',
        '^#(?:[0-9a-fA-F]{1,2}){3}$'
    )
