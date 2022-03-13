
from blogpackage.models import Post
from flask import Blueprint, render_template, request

main=Blueprint('main', __name__)

# route decorators tells flask what URL triggers the function.
@main.route("/")
@main.route("/home")
def home():
    # get the 'page' query parameter in the URL; default to page 1, page can only = integer
    page = request.args.get('page', default=1, type=int)
    # query posts in order of descending post date. posts is a paginate object (limit 3 posts/ page)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts, title="Home - Cally's Programming Brain Dump")


@main.route("/about")
def about():
    return render_template('about.html', title='About')
