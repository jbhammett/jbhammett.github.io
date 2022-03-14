Social Distancing Activities Videos

This project allows users to create an account and to post videos. The intended theme of videos is social distancing activities. Users can like posts, and they can edit their own posts. Each post can be assigned to a category, and users can then view all posts within each category by selecting a link on the Categories page. Users can also access all posts by an individual user by clicking on a username. A description of each file is below.

index.html
This page shows all posts by all users in reverse chronological order.

categories.html
This page allows users to select a category of posts to view.

category.html
This page shows all posts within the specific category selected by a user.

create.html
This page contains a form where users can create posts and upload videos.

layout.html
This file contains common code for the html files such as the links to create a page or to view categories.

login.html (Used file provided in project 4)
This page contains a form for registered users to login.

profile.html
This page shows all posts of a specific user.

register.html (Used file provided in project 4)
This page contains a form where users can register for the site.


social.js
This file contains event listeners and functions to allow users to like posts or to edit their own posts when they click a button.


style.css 
This file contains class styling for posts, edit button, like button, timestamps, usernames, and videos.


forms.py
This file contains the form used on create.html to create a new post.

models.py
This form contains the User, Post, and Category models. 

urls.py
This file contains the url to each of the views in views.py.

util.py
This file contains a function to track the liked posts of the user who is logged in. It is used in several functions in views.py.

views.py
This file contains the following functions: index(), login_view(), logout_view(), register(), create_post(), edit_post(), like_posts(), categories(), category_posts(),
and profile().