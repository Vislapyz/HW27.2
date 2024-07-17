from rest_framework.exceptions import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube = "https://www.youtube.com/"
        link = value.get(self.field)
        if link and (youtube not in link):
            raise ValidationError("Ссылка должна быть на YouTube")
