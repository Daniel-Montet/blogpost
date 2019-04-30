import secrets
import os
from flask import render_template, flash, redirect,url_for, request, abort,Blueprint
from app.posts.forms import PostForm, CommentForm
from app.models import Pitch, Comment
from app import db
from flask_login import current_user,login_required
from app.posts.utils import save_picture, save_video


posts = Blueprint('posts',__name__)


@posts.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!','success')
        hashtag=''
        hashtags= form.content.data
        print(hashtags)
        newstr= hashtags.split()
        for char in newstr:
            if char.startswith("#"):
                hashtag=char.strip("#")
                print(hashtag)
                # if form.picture.data:
                #     picture_file = save_picture(form.picture.data)
                picture_file = save_picture(form.picture.data)
                # video_file = save_video(form.video.data )
                image = url_for('static',filename='images/'+picture_file)
 
                # video = url_for('static',filename='videos/'+video_file)

                post = Pitch(title = form.title.data, content= form.content.data, author = current_user,hashtags=hashtag
                                    ,image = image)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('main.home'))
        
    return render_template('create_post.html', title='New Post',form=form,legend='New Post') 

@posts.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    review= CommentForm()
    comments = Comment.query.all()
    post = Pitch.query.get_or_404(post_id)
    if review.validate_on_submit():
        # if review.picture.data:
        #             picture_file = save_picture(review.picture.data)
                    

        # if review.video.data:
        #             video_file = save_video(review.video.data)
        picture_file = save_picture(review.picture.data)
        image = url_for('static',filename='images/'+picture_file)           
        comment = Comment(body= review.comment.data,post_id=post.id,image_file = image)
        db.session.add(comment)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    return render_template('post.html',title = post.title, post=post,review=review, comments = comments )

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Pitch.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # form.title.data = post.title
    # form.content.data = post.content
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Updated Post')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
    form=form,legend='Update Post')

@posts.route("/post/<int:post_id>/delete",methods=['GET','POST'])
def delete_post(post_id):
    post = Pitch.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main.home'))

@posts.route("/post/<int:post_id>/delete",methods=['GET','POST'])
def delete_comment(post_id):
    post = Comment.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your comment has been deleted!','success')
    return redirect(url_for('main.home'))

