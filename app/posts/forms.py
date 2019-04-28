from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileAllowed,FileField
from wtforms.validators import DataRequired, DataRequired



class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    picture = FileField('Update Profile Picture')
    video = FileField('Update Intro Video')
    submit = SubmitField('Post', validators=[FileAllowed('jpg','png'),FileAllowed('mp4','gif')])


class CommentForm(FlaskForm):
    comment = TextAreaField('comment',validators=[DataRequired()])
    picture = FileField('Update Profile Picture')
    video = FileField('Update Intro Video')
    submit = SubmitField('Post', validators=[FileAllowed('jpg','png'),FileAllowed('mp4','gif')])
    
