# Reddit knockoff

## Routes

### /

- Redirects to /register

### /image/<image_path>.png

- Dynamic path to user's uploaded profile picture

### /app/

- VueJS app endpoints for profile and feed. Async requests made to /api
endpoints for content rendering.

####/app/profile/<user_hash>

- Profile page for user, allows creation and deletion of posts

#### /app/feed/<user_hash>

- Feed page for user with async up and down voting

### /gettsv

- Renders template with three download options for users, posts, and votes

#### /gettsv/[user/post/vote]

- Redirects to correct download link

#### /gettsv/download/[user/post/vote].tsv

- Retrieves a saved tsvfile

### /register
 
- Account creation page
- Redirects to /app/feed/<user_hash> of registered user

### /posts/<post_id>

- Individual post page for <post_id>

### /<user_hash>/vote/<post_id>/[up/down]

- Instructs an upvote or downvote emenating from a user (user_hash) to a post (post_id)
- Returns JSON object with parameter 'tally' mapping to 
    the new vote count
  
### /<user_hash>/create

- Returns form for user to type a new post with a title.
- Redirects to user's profile
    
### /api/

- post JSON schema:
    ```
    {
        'handle': str,
        'post_votes': int,
        'post_content': str,
        'post_creator': str,
        'post_timestamp': str,
        'post_id': int,
        'time_passed': str
    }
  ```

#### /api/<user_hash>/profile

- Returns array of posts which user (user_hash) 
has created, post objects follow post JSON schema
  
#### /api/<user_hash>/feed

- Returns array of posts which all but user (user_hash) have
    created. Post objects follow post JSON schema.
  
#### /api/<user_hash>/delete/<post_id>

- Deletes the post (post_id) which the user (user_hash) created
- returns JSON object with key 'status' mapping to 'ok'


