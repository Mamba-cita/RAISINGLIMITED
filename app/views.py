from app import app,LoginManager,login_manager,db
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app.forms import LoginForm,RegisterForm,PostsForm,SearchForm
from app.models import User,Posts,Shipments,Orders
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os








@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#decorator to use for every view
#admin page

#website home page

@app.route('/')
def index():
    return render_template('web_index/templates/index.html')




#blog posts


@app.route('/blogs')
def blogs():
    posts=Posts.query.order_by(Posts.date_created)
    return render_template('web_index/templates/blogs.html',posts=posts)


#protected routes for blog posts

#add a blog post

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    name=None
    form = PostsForm()
    if form.validate_on_submit():
        poster = current_user.id
        #create a new post
        post = Posts(title=form.title.data, body=form.body.data, poster_id=poster, slug=form.slug.data)
        #clear the form
        form.title.data = ''
        form.body.data = ''
        form.slug.data = ''
        #add the post to the database
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        #return redirect(url_for('blogs'))
    return render_template('web_index/templates/add_post.html', form=form, name=name)

#individual blog post

@app.route('/blog/<id>')
def blog(id):
    post = Posts.query.get_or_404(id)
    return render_template('web_index/templates/blog.html', post=post)
    

#edit a blog post

@app.route('/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostsForm()
    if form.validate_on_submit():
            #grab the post from the database
            post.title = form.title.data
            post.body = form.body.data
            post.slug = form.slug.data
            #commit the changes to the database
            db.session.add(post)
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('blog', id=post.id))
    if current_user.id == post.poster_id:
    #display data in edit form
        form.title.data = post.title
        form.body.data = post.body
        form.slug.data = post.slug
        return render_template('web_index/templates/edit_post.html',form=form, post=post)
    else:
        flash('You are not authorized to edit this post.', 'danger')
        posts=Posts.query.order_by(Posts.date_created)
        return render_template('web_index/templates/blogs.html',posts=posts)


#delete a blog post

@app.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster_id:
    #delete the post from the database
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Your post has been deleted!', 'success')
            return redirect(url_for('blogs'))
        except:
            flash('Your post could not be deleted!', 'error')
            return redirect(url_for('blogs'))
    else:
        flash('You do not have permission to delete this post!', 'error')
        return redirect(url_for('blogs'))



#end of protected routes for blog posts


#internal app routes

#Registration page

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    name=None
    form = RegisterForm()
    #validation of form
    if form.validate_on_submit():
        #check if user already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            #create a new user
            user = User(
                name=form.name.data, 
                email=form.email.data, 
                )
            #set password
            user.set_password(form.password.data)
            
            #add user to db
            db.session.add(user)
            db.session.commit()
            #flash message
            flash('You have been registered successfully')
            #clear form
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            form.confirm_password.data = ''
            #redirect to login page
            return redirect(url_for('login'))
    return render_template('internal_app/templates/register/register.html', form=form, name=name)\
        
        
#update user profile

@app.route('/update_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def update_profile(id):
    form = RegisterForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        
        
        #check for profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']
            #grab image name
            pic_name = secure_filename(name_to_update.profile_pic.filename)
            
            #set uuid for image name
            pic_uuid = str(uuid.uuid4()) + '_' + pic_name
                #save image to folder
            name_to_update.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_uuid))
            #change image name
            name_to_update.profile_pic  = pic_uuid
            #update db
            try:
                db.session.commit()
                flash('Your profile has been updated!', 'success')
                return render_template('internal_app/templates/users/profile/update_profile.html', form=form, name=name_to_update)
            except:
                flash('Your profile could not be updated!', 'error')
                return render_template('internal_app/templates/users/profile/update_profile.html', form=form, name=name_to_update)
        else:
             db.session.commit()
             flash('Your profile has been updated!', 'success')
             return render_template('internal_app/templates/users/profile/update_profile.html', form=form, name=name_to_update)
    else:
        return render_template('internal_app/templates/users/profile/update_profile.html', form=form, name=name_to_update)
       
 #Remove user profile
@app.route('/delete_profile/<int:id>')
@login_required
def delete_profile(id):
        user_to_delete = User.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Your profile has been deleted!', 'success')
            return redirect(url_for('users'))
        except:
            flash('Your profile could not be deleted!', 'error')
            return render_template('internal_app/templates/users/users.html')    
        
        
        
#users page

@app.route('/users')
@login_required
def users():
    user= User.query.all()
    return render_template('internal_app/templates/users/users.html', user=user)


#user dashboard page

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('internal_app/templates/users/users_dashboard.html')





# #user profile






#Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    name =None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            #check password
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('user not found', 'danger')
            
    return render_template('internal_app/templates/login/login.html', form=form, name=name)




#protected routes

#home page


@app.route('/home')
@login_required
def home():
    shipments = Shipments.query.order_by(Shipments.created_at)
    return render_template('internal_app/admin/home/home.html', shipments=shipments)
                          



#internal blog routes
@app.route('/blogs_internal')
@login_required
def blogs_internal(): 
    posts=Posts.query.order_by(Posts.date_created)
    return render_template('home/blogs_internal/blogs_internal.html',posts=posts)



#add a blog post

@app.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    name=None
    form = PostsForm()
    if form.validate_on_submit():
        poster = current_user.id
        #create a new post
        post = Posts(title=form.title.data, body=form.body.data, poster_id=poster, slug=form.slug.data)
        #clear the form
        form.title.data = ''
        form.body.data = ''
        form.slug.data = ''
        #add the post to the database
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        #return redirect(url_for('blogs'))
    return render_template('home/blogs_internal/create_blog.html', form=form, name=name)


#individual blog post

@app.route('/single_blog_internal/<id>')
def single_blog_internal(id):
    post = Posts.query.get_or_404(id)
    return render_template('home/blogs_internal/single_blog_internal.html', post=post)
    

#jjjjjjjjjjjjjj
#edit a blog post

@app.route('/update_blogs_internal/<id>', methods=['GET', 'POST'])
@login_required
def update_blogs_internal(id):
    post = Posts.query.get_or_404(id)
    form = PostsForm()
    if form.validate_on_submit():
            #grab the post from the database
            post.title = form.title.data
            post.body = form.body.data
            post.slug = form.slug.data
            #commit the changes to the database
            db.session.add(post)
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('blogs_internal', id=post.id))
    if current_user.id == post.poster_id:
    #display data in edit form
        form.title.data = post.title
        form.body.data = post.body
        form.slug.data = post.slug
        return render_template('home/blogs_internal/update_blogs_internal.html',posts=posts)
    else:
        flash('You are not authorized to edit this post.', 'danger')
        posts=Posts.query.order_by(Posts.date_created)
        return render_template('home/blogs_internal/update_blogs_internal.html',posts=posts)


#delete a blog post

@app.route('/delete_blog_internal/<int:id>')
@login_required
def delete_blog_internal(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster_id:
    #delete the post from the database
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Your post has been deleted!', 'success')
            return redirect(url_for('blogs_internal'))
        except:
            flash('Your post could not be deleted!', 'error')
            return redirect(url_for('blogs'))
    else:
        flash('You do not have permission to delete this post!', 'error')
        return redirect(url_for('blogs_internal'))



# shipments


@app.route('/shipments', methods=['GET', 'POST'])
@login_required
def shipments():
    shipments = Shipments.query.order_by(Shipments.created_at)
    return render_template('internal_app/admin/home/shipments.html', shipments=shipments)



#shipment creation

@app.route('/shipments_creation', methods=['GET', 'POST'])
@login_required
def shipments_creation():
    return render_template('internal_app/admin/home/shipments_creation.html')

#order creation
@app.route('/order_creation', methods=['GET', 'POST'])
@login_required
def order_creation():
    return render_template('internal_app/admin/home/order.html')



#pass data to  the navbar

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)
    


#search 
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    posts = Posts.query.all()
    if form.validate_on_submit():
        searched = form.searched.data
        #query the database from navbar search
        posts = Posts.query.filter(Posts.body.like('%' + searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template('web_index/search.html', form=form, searched=searched, posts=posts)
        
   

#admin page

@app.route('/admin')
@login_required
def admin():
    return render_template('internal_app/admin//admin.html')



#logout page

@app.route('/afri_home', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))
    











