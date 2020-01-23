# MyWishList
## Authors: Jack Miller and Xiaoxuan Zhang
## App Link: https://still-garden-91097.herokuapp.com/login
## Api Useage: Ebay api
Introduction: This project is a wish list. This project allows the user to search ebay for products adding them to a wishlist. Users can have multiple wish lists and other users can view their own wish list or their friend's wish lists by searching using their email.
Pages description: 
1.login: a landing page where the user logs in to their account register: a new user can create a new account 2.logout: user can logout of their account 3.index: landing page for users with two forms one for finding a submitted wishlist and one for creating a new wish list newlist: creates a new wish list search: uses ebay api to search for items adding them to products and displaying rename: allows user to rename the current wishlist add/delete: adds/delete a new product to the current wish list
-Login and register page for getting the user set up -Index page for choosing whether to look up a created wish list or creating a new list -Create new page to search the ebay products and choose ones to add to wish list -Wish list page to find other user's wish lists
-Login: id, username, password. Used to log users in -User: my_id, username,l_name, f_name, email. Stores data for the user with a name and email for searching -Wishlist: wish_id, user_id, time, name, comments. Wishlist to store new lists of products -Product: product_id, name, price, category, url. Product is a list of products to pull from for wishlist -Granted: gid, product_id, wishList_id, time. A list that matches a product to a wishlist
User login: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins More login: https://www.youtube.com/watch?v=q7HVghYjwYo&t=620s
