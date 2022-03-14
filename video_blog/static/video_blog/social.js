document.addEventListener('DOMContentLoaded', function() {
  // Hide all edit forms for each post initially
  document.querySelectorAll('.edit_body').forEach(form => {
    form.style.display = 'none'
  })

  // Add event listeners to edit buttons for each post
  document.querySelectorAll('.edit').forEach(button => {
    button.onclick = function(){ 
      edit_post(this.dataset.post)
    }
  })

  // Add event listeners to like buttons for each post
  document.querySelectorAll('.like').forEach(like=> {
    like.addEventListener('click', () => like_post(like));
  });

});


// If editing, hide body, show form, and add body to inital value.
// Otherwise, body should show on form.
function edit_post(post){
  const postId = post;
  document.querySelector(`.post_body[data-post="${postId}"]`).style.display = 'none';
  document.querySelector(`.edit_body[data-post="${postId}"]`).style.display = 'block';
  document.querySelector(`.submit_edit[data-post="${postId}"]`).addEventListener('click', () => submit_edit(post));    
}



// Submit user's edits to edit_post function. 
function submit_edit(post){
  const postId = post;
  const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  fetch(`/edit/${postId}`,{
      method: 'PUT',
      body: JSON.stringify({
            content: document.querySelector(`.new_body[data-post="${postId}"]`).value
      }),
       headers: {
            "X-CSRFToken": token
    }
  })
  .then(response => response.json())
  // Display editted post and hide edit form
  .then(data => {
    document.querySelector(`.post_body[data-post="${postId}"]`).innerHTML = 
      document.querySelector(`.new_body[data-post="${postId}"]`).value;
    document.querySelector(`.post_body[data-post="${postId}"]`).style.display = 
      'block';
    document.querySelector(`.edit_body[data-post="${postId}"]`).style.display = 'none';
  });
  return false;
}


// Allow user to like or unlike a post
function like_post(like){ 
  const id = like.dataset.post;
  const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  const liked = like.dataset.liked === "1" ? false : true;
  
  // Send fetch request to like_post function  
  fetch(`/likes/${id}`,{
    method: 'PUT',
    body: JSON.stringify({
      liked: liked
    }),
    headers: {
      "X-CSRFToken": token
    }
  })
  .then(response => response.json())
  .then(data => {       
    // Track whether post is liked or not
    if (liked) {
      like.dataset.liked = "1";

      // Change like button to unlike if post is liked by user
      document.querySelector(`.like[data-post="${id}"]`)
      .innerHTML = "Unlike";
    } else {
      like.dataset.liked = "0";

      // Change button to like if post is not liked by user
      document.querySelector(`.like[data-post="${id}"]`)
      .innerHTML = "Like";
    }
    
    // Set the like count
    document.querySelector(`.like_count[data-post="${id}"]`)
    .innerHTML = data.user_likes;  
    });
}
