"""CMS forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, SelectField, StringField, TextAreaField
from wtforms.fields import DateField, EmailField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from ..theme import FONT_CHOICES

IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]
IMAGE_VALIDATOR = FileAllowed(IMAGE_TYPES, "Images only (jpg, png, webp).")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])


class ContentForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    slug = StringField(
        "Slug",
        validators=[
            Optional(),
            Length(max=200),
            Regexp(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", message="Lowercase letters, numbers and hyphens only."),
        ],
    )
    summary = TextAreaField("Summary", validators=[Optional()])
    body = TextAreaField("Content", validators=[Optional()])
    image = FileField("Image", validators=[IMAGE_VALIDATOR])
    remove_image = BooleanField("Remove current image")
    date = DateField("Date", validators=[Optional()])
    external_url = URLField("External URL", validators=[Optional(), URL(), Length(max=500)])
    is_published = BooleanField("Published", default=True)


class HeroForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    subtitle = TextAreaField("Subtitle", validators=[Optional()])
    image = FileField("Image", validators=[IMAGE_VALIDATOR])
    remove_image = BooleanField("Remove current image")
    button_text = StringField("Button text", validators=[Optional(), Length(max=80)])
    button_url = StringField("Button URL", validators=[Optional(), Length(max=500)])


class PortfolioForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=150)])
    position = StringField("Position", validators=[Optional(), Length(max=150)])
    bio = TextAreaField("Biography", validators=[Optional()])
    expertise = TextAreaField("Expertise (comma separated)", validators=[Optional()])
    linkedin_url = URLField("LinkedIn URL", validators=[Optional(), URL(), Length(max=500)])
    image = FileField("Photo", validators=[IMAGE_VALIDATOR])
    remove_image = BooleanField("Remove current photo")


class ContactForm(FlaskForm):
    phone = StringField("Phone number", validators=[Optional(), Length(max=60)])
    address = TextAreaField("Address", validators=[Optional()])
    email = EmailField("Email address", validators=[Optional(), Length(max=150)])


class FontForm(FlaskForm):
    font_heading = SelectField("Heading font", choices=FONT_CHOICES)
    font_body = SelectField("Body font", choices=FONT_CHOICES)


class PaletteForm(FlaskForm):
    name = StringField("Palette name", validators=[DataRequired(), Length(max=80)])
