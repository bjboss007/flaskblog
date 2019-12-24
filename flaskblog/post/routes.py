from flask import redirect, url_for, render_template, request, flash, Blueprint
from flask_login import current_user, login_required
from flaskblog import bcrypt, db
from flaskblog.models import Post, User
from .forms import CreatePost

posts = Blueprint('posts',__name__)


@posts.route('/post_new', methods = ['GET', 'POST'])
@login_required
def new_post(): 
    form = CreatePost()

    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            content = form.content.data,
            author = current_user
        )
        db.session.add(post)
        db.session.commit()
        flash(f'Post successfully created','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)    
    return render_template('post.html', post = post, title = post.title, legend = 'Update Post')


@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CreatePost()
    
    if not(current_user.is_authenticated and current_user == post.author):
        flash(f'You can not edit this post, You are not the author','warning')
        return redirect(url_for('posts.post', post_id = post.id))

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Post successfully updated', 'success')
        return redirect(url_for('posts.post', post_id = post.id))
        
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", form = form , title = 'Update Post', legend = 'Update Post')

@posts.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if not(current_user.is_authenticated and current_user == post.author):
        flash(f'You can not delete this post, You are not the author','warning')
        return redirect(url_for('main.home'))
    else:
        db.session.delete(post)
        db.session.commit()
        flash(f'Post successfully deleted','success')
        return redirect(url_for('main.home'))