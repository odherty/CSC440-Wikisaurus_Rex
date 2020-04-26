"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import current_app
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.datastructures import MultiDict

from wiki.core import Processor
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web.forms import UserForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect
<<<<<<< HEAD
from wiki.web.user import UserManager
from wiki.web.user import User
#from Riki import app
=======

from wiki.web.history import update_history, get_history_id, format_history_id

import os
>>>>>>> c8cc53c38f0383d0720562269d4a0766e239059a

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
    user = current_user.get("roles")
    isAdmin = False
    if user == ['admin']:
        isAdmin = True
    return render_template('index.html', pages=pages, isAdmin = isAdmin)


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


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    user = current_users
    usermanager = UserManager.read(user)
    if current_user.get("roles") != ["admin"]:
        flash("You do not have the permissions to see this page")
        return render_template('index.html')

    return render_template('user.html', usermanager = usermanager)


@bp.route('/user/create/', methods=['GET', 'POST'])
def user_create():
    form = UserForm()
    user = UserManager(current_app.config['USER_DIR'])

    if form.validate_on_submit():
        if form.admin.data:
            roles = ['admin']
        else:
            roles = ''
        user.add_user(form.name.data, form.password.data, True, roles, None)
        return redirect(url_for("wiki.user_index"))

    return render_template('usercreate.html', form=form)

 
@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass

@bp.route('/user/update/<user_name>/', methods=['GET',"POST"])
def user_update(user_name):
    usermanager = UserManager(current_app.config["USER_DIR"])
    user = usermanager.get_user(user_name)
    form = UserForm()
    
    
    if form.validate_on_submit():
        if form.admin.data:
            userdata = {"active": True, "authentication_method": "cleartext", "password":form.password.data, "authenticated": True, "roles":['admin']}
        else:
            userdata = {"active": True, "authentication_method": "cleartext", "password":form.password.data, "authenticated": True, "roles":[]}
        usermanager.update(user_name, userdata)
        return redirect(url_for("wiki.user_index"))
    return render_template('update.html', form = form, user_name = user_name, password = user.get('password'))


@bp.route('/user/delete/<user_name>/', methods=["POST"])
def user_delete(user_name):
    user = UserManager(current_app.config['USER_DIR'])

    user.delete_user(user_name)
    return redirect(url_for("wiki.user_index"))
    


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

<<<<<<< HEAD
=======

@bp.route('/history/<path:url>/', methods=['GET', 'POST'])
@protect
def history_list(url):
    path = current_wiki.history_path(url)
    # if history path doesn't exist, show no history page

    page = current_wiki.get(url)

    # no history or non-existent page, show the no history page
    if not os.path.exists(path) or page is None:
        return render_template("no_history.html", page_name=url)

    file_ids = []
    links = []
    link_names = []

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

        link_name = format_history_id(file_id)
        link_names.append(link_name)

    return render_template('history_list.html', page=page, file_ids=file_ids, links=links, link_names=link_names)


@bp.route('/history_page/<id>/<path:url>/', methods=['GET', 'POST'])
@protect
def history_page(id, url):
    # build the url to the history page
    url = "history/" + url + "/" + id

    page = current_wiki.get_or_404(url)

    # modify the title to include that it is an archived version
    page.title = page.title + " (Old Revision: " + format_history_id(id) + ")"

    return render_template('history_page.html', page=page)
>>>>>>> c8cc53c38f0383d0720562269d4a0766e239059a
