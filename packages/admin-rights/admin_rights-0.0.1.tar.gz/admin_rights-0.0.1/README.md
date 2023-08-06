## Admin Protected Route

This is a function that takes an array of users as an argument and checks if the role is an admin.
If that isn't the case, the function returns an unauthorized status code and message. 
Otherwise, the user is permitted to use the function. 