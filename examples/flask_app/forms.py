from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class UploadImage(FlaskForm):
    image = FileField(
        "Your Image",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "jpeg", "png", "gif"], "Please upload image files only!"
            ),
            InputRequired(),
        ],
    )
    upload = SubmitField("Upload Image")


class ResampleImage(FlaskForm):
    colors = IntegerField(
        "Max Colors", validators=[InputRequired(), NumberRange(min=1, max=20)]
    )
    sensitivity = IntegerField(
        "Sensitivity", validators=[InputRequired(), NumberRange(min=0, max=250)]
    )
    resample = SubmitField("Resample Colors", validators=[InputRequired()])
