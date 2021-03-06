import re

from unicodedata import normalize

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _


# hidden auth fields
HIDDEN_AUTH_FIELDS = {
    "is_active": forms.HiddenInput(),
    "created_on": forms.HiddenInput(),
    "modified_on": forms.HiddenInput(),
    "made_by": forms.HiddenInput(),
}

# choices for some fields
COUNTRIES = (("BR", _("Brazil")), ("US", _("United States")))
GENDER_TYPES = (
    ("M", _("male")),
    ("F", _("female")),
)
EMPLOYEE_CLASS = (
    ("SEN", _("Senior")),
    ("TRN", _("Trainee")),
    ("FRE", _("Freelancer")),
    ("VOL", _("Volunteer")),
)


def sanitize_name(name):
    return " ".join([w.lower().capitalize() for w in name.split()])


def us_inter_char(txt, codif="utf-8"):
    if not isinstance(txt, str):
        txt = str(txt)
    return (
        normalize("NFKD", txt)
        .encode("ASCII", "ignore")
        .decode("ASCII")
        .lower()
    )


def short_name(name):
    words = name.split(" ")
    if len(words) <= 2:
        return name
    # get first and last words of name
    first_word = words[0]
    words.pop(0)
    last_word = words[-1]
    words.pop()
    # make a list to join
    to_join = [first_word]
    for word in words:
        if len(word) <= 3:
            to_join.append(word.lower())
        else:
            to_join.append(f"{word[0]}.")
    to_join.append(last_word)
    return " ".join(to_join)


def cpf_validation(num):
    cpf = "".join(re.findall(r"\d", num))

    if len(cpf) != 11:
        return False
    if cpf in (
        "00000000000",
        "11111111111",
        "22222222222",
        "33333333333",
        "44444444444",
        "55555555555",
        "66666666666",
        "77777777777",
        "88888888888",
        "99999999999",
    ):
        return False

    weight1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    digit1 = 11 - (
        sum([int(d) * weight1[n] for n, d in enumerate(cpf[:9])]) % 11
    )
    if digit1 > 9:
        digit1 = 0

    if cpf[9:10] != f"{digit1}":
        return False

    weight2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    digit2 = 11 - (
        sum([int(d) * weight2[n] for n, d in enumerate(cpf[:9] + str(digit1))])
        % 11
    )
    if digit2 > 9:
        digit2 = 0

    if cpf[9:] != f"{digit1}{digit2}":
        return False

    return True


def cpf_format(num):
    cpf = "".join(re.findall(r"\d", num))
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message=_(
        "Phone number must be entered in the format: '+1234567890'. \
            Up to 15 digits allowed."
    ),
)


def phone_format(num, country="BR"):
    num = (
        "+{}".format("".join(re.findall(r"\d", num)))
        if num.startswith("+")
        else "".join(re.findall(r"\d", num))
    )

    if not num:
        return ""

    if country == "BR":
        if num.startswith("+"):
            num = (
                f"+{num[1:3]} {num[3:5]} {num[5:10]}-{num[10:]}"
                if len(num) == 14
                else f"+{num[1:3]} {num[3:5]} {num[5:9]}-{num[9:]}"
            )
        elif len(num) in (10, 11):
            num = (
                f"+55 {num[:2]} {num[2:7]}-{num[7:]}"
                if len(num) == 11
                else f"+55 {num[:2]} {num[2:6]}-{num[6:]}"
            )

    return num


def paginator(queryset, limit=10, page=1):
    paginator = Paginator(queryset, limit)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    return object_list


def clear_session(request, items):
    for item in items:
        if request.session.get(item):
            del request.session[item]
