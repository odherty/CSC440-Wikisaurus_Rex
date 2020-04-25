"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import UserUpdateForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect

from wiki.web.history import update_history, get_history_id

import os  # temporary, remove later

bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        update_history(url)
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)

@bp.route('/<path:url>/related/')
@protect
def related(url):
    # get url
    page = current_wiki.get_or_404(url)

    # make list of tags about original article
    tags = page.tags
    tagslist =  tags.split(", ")

    #blank list to hold other articles with the same tags
    tagged = []
    for i in tagslist:
        # append tag category
        tagged.append(i.capitalize())
        #check if list of articles is only the original article, if not then add the article
        if len(current_wiki.index_by_tag(i)) > 1:
            tagged += current_wiki.index_by_tag(i)
        #if there are no other articles other than the orignal article, append this statement
        else:
            tagged.append("No other wikis with this tag")
      
    return render_template('related.html', tags=tagslist, page = page, pages = tagged)

@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/<string:username>', methods=['GET', 'POST'])
def user_display(username):
    user = current_users.get_user(username)
    form = UserUpdateForm()
    if form.validate_on_submit():
        if form.password.data != '':
            current_user.set('password', form.password.data)
        if form.email.data != '':
            current_user.set('email', form.email.data)
        flash('Profile Updated!', 'success')
    return render_template('user.html', user=user, form=form)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        user.set('active', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    current_user.set('active', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/')
def user_create():
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@bp.route('/history/<path:url>/', methods=['GET', 'POST'])
@protect
def history_list(url):
    path = current_wiki.history_path(url)
    # if history path doesn't exist, show no history page

    page = current_wiki.get(url)

    # no history or non-existent page
    if not os.path.exists(path) or page is None:
        return render_template("404.html")

    file_ids = []
    links = []

    for filename in os.listdir(path):
        if filename.endswith(".md"):
            file_ids.append(get_history_id(filename))
            continue
        else:
            continue

    # show in reverse chronological order (most recent first)
    file_ids.reverse()

    for file_id in file_ids:
        page_link = "/history_page/" + file_id + "/" + url
        links.append(page_link)

    return render_template('history_list.html', page=page, file_ids=file_ids, links=links)


@bp.route('/history_page/<id>/<path:url>/', methods=['GET', 'POST'])
@protect
def history_page(id, url):
    # build the url to the history page
    url = "history/" + url + "/" + id

    page = current_wiki.get_or_404(url)

    # modify the title to include that it is an archived version
    page.title = page.title + " (Old Revision: " + id + ")"

    return render_template('history_page.html', page=page)
