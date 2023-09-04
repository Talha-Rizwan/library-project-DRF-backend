# Library_management_system

ALL API Details:


-> Book Apis


Api : to create a book object in library: (authentication needed, user role ‘admin’ or ‘role’)
Url : http://127.0.0.1:8000/api/book-view-set/
Method : Post
Body:
 {
"name": "Now you see me",
"author_name": "dale",
"publisher_name": "dale",
"number_of_books": 5
}

Api : to get all books in library: 
Url : http://127.0.0.1:8000/api/book-view-set/
Method : Get

Api : to get a single book
Url : http://127.0.0.1:8000/api/book-view-set/id/
Method : Get

Api : to update a book (authentication needed, user role ‘admin’ or ‘role’)
Url : http://127.0.0.1:8000/api/book-view-set/id/
Method : Put
Body: 
{
"id": 37,
"name": "Now you see me",
"author_name": "Thomas",
"publisher_name": "dale",
"number_of_books": 5
}

Api : to delete a book (authentication needed, user role ‘admin’ or ‘role’)
Url : http://127.0.0.1:8000/api/book-view-set/id/
Method : Delete

Api : to get books by their name or author name (not exact name necessary)
Url : http://127.0.0.1:8000/api/book-detail-name/the
Method : Get


-> User Apis:


Api : to register a new user 
Url : http://127.0.0.1:8000/api/user-profile/
Method : Post
Body: 
{
"username": "ali",
"full_name": "Qasim Rizwan",
"password": "Talha@2000",
"gender" : "M",
"phone": "00039383"
}

Api : to login user (get jwt authentication token)
Url : http://127.0.0.1:8000/api/login/
Method : Post
Body: 
{
"username": "ali",
"password": "Talha@2000"
}

Api : to update user profile
Url : http://127.0.0.1:8000/api/user-profile/
Method : Put
Body: 
{
"full_name": "Rizwan Malik"
}


Api : get all users (only librarian/admin)
Url : http://127.0.0.1:8000/api/users/
Method : GET

Api : Get a single user and its role (only admin)
Url : http://127.0.0.1:8000/api/user-role/1/
Method : GET

Api : Update a user role (only admin)
Url : http://127.0.0.1:8000/api/user-role/1/
Method : PUT
Body: 
{
"id": 1,
"username": "admin",
"role": "A"
}




-> Request Apis


Api : to get a user’s  pending book requests (logged in user)
Url : http://127.0.0.1:8000/api/user-request/
Method : GET

Api : to create a user pending book request (logged in user)
Url : http://127.0.0.1:8000/api/user-request/
Method : POST
Body: 
{
"requested_book": 2,
"status": "P"
}

Api : librarian to get list of all the pending requests (only librarian)
Url : http://127.0.0.1:8000/api/all-request/
Method : Get

Api : get a specific request (only librarian)
Url : http://127.0.0.1:8000/api/request/3/
Method : Get

Api : change a specific request status (only librarian) 
Description : In case of ‘A’, the book will be added to the issued_books attribute of the request generator user and the number on copies of that book will be decreased by 1, nothing happens if ‘R’ is sent by librarian 
Url : http://127.0.0.1:8000/api/request/3/
Method : Put
Body: 
{
"status": "A"
}

Api : user initiate a Return request to give the book back to the library
Url : http://127.0.0.1:8000/api/return-request/8/
Method : Put
Body: 
{
"status" : "B"
}

Api : to close a Return Back request, (only librarian)
Description : if a user has initiated a return back request, only then the admin or librarian can close the request. This will remove the book from the issued books attribute of the user and add 1 in the total number of copies available for that book.
Url : http://127.0.0.1:8000/api/close-request/7/
Method : Put
Body: 
{
"status": "C"
}


Extra Functionality APIs:


Api : Librarian can see all the delayed book issued requests (with status approved only) (only librarian)
Url : http://127.0.0.1:8000/api/home/delay-request/
Method : Get


Api : Librarian can get a specific delayed book issued request (with status approved only) (only librarian)
Url : http://127.0.0.1:8000/api/home/delay-request/11
Method : Get


Api : Librarian can send email to delayed requests users to return book (with status approved only)  (only librarian)
Url : http://127.0.0.1:8000/api/home/delay-request/11/send_mail/
Method : Post


Api : User can create a ticket if a book is not available and email send to librarian
Url : http://127.0.0.1:8000/api/home/ticket/
Method : POST
Body: 
{
"book_name": "silent killer",
"status": "P"
}


Api : librarian can get all the pending tickets 
Url : http://127.0.0.1:8000/api/home/ticket/
Method : GET


Api : librarian can get a single pending ticket request
Url : http://127.0.0.1:8000/api/home/librarian-ticket/3/
Method : GET


Api : librarian can reject the pending ticket by giving a reason which will be sent to the user as email.
Url : http://127.0.0.1:8000/api/home/librarian-ticket/3/
Method : Put
Body: 
{
"status": "R",
"reason": "not good"
}


Api : librarian can approve the pending ticket by creating a new book object and email will be sent to the user.
Url : http://127.0.0.1:8000/api/home/librarian-ticket/3/
Method : Put
Body:  
{
"status": "A",
"book_name": "new book 3",
"author_name" : "abc",
"publisher" : "test",
"number_of_copies": 10
}
