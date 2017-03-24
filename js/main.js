function verifyDeletePost(postID) {
  $('#delete-post-dialog').dialog();
  $('#delete-post-dialog [name=delete]').attr('onclick', 'deletePost(' + String(postID) + ')');
}

function deletePost(postID) {
  $.post({
    url : '/deletepost/' + String(postID),
    success: function() {
        $('#' + String(postID)).remove();
        $('#delete-post-dialog').dialog('close');
        alert('Post deleted!');
    }
  });
}

function closeDialog() {
  $('.dialog').dialog('close');
}

function likePost(postID) {
  $.post({
    url : '/likepost/' + String(postID),
    success: function() {
      // toggle to unlike
      $('#' + postID + ' .like-button').text('Unlike');

      // change onclick to unlike function
      oldFunc = $('#' + postID + ' .like-button').attr('onclick');
      newFunc = oldFunc.replace('like', 'unlike');
      $('#' + postID + ' .like-button').attr('onclick', newFunc);

      // increment like-count
      likeCount = parseInt($('#' + postID + ' .like-count').text());
      $('#' + postID + ' .like-count').text(likeCount + 1);
    },
    error: function() {
      alert("Not allowed to like!");
    }
  });
}

function unlikePost(postID) {
  $.post({
    url: '/unlikepost/' + String(postID),
    success: function() {
      // toggle to unlike
      $('#' + postID + ' .like-button').text('Like');

      // change onclick to like function
      oldFunc = $('#' + postID + ' .like-button').attr('onclick');
      newFunc = oldFunc.replace('unlike', 'like');
      $('#' + postID + ' .like-button').attr('onclick', newFunc);

      // increment like-count
      likeCount = parseInt($('#' + postID + ' .like-count').text());
      $('#' + postID + ' .like-count').text(likeCount - 1);
    },
    error: function() {
      alert("Not allowed to unlike!");
    }
  });
}

function addComment(postID) {
  var commentText = $('#' + String(postID) + ' input[name="comment"]')[0].value
  $.post({
    url:  '/addcomment/' + String(postID),
    data: {'comment': commentText},
    success: function(response) {
      // create new comment section without refreshing
      var comment = JSON.parse(response);
      var $newCommentSection = $.parseHTML(
        `<section class="comment" id="${comment.id}">
            <p class="comment-text">
                ${comment.comment}
            </p>
            <div class="comment-footer">
                <div class="comment-likes">
                    <span class="like-comment-button">👍</span>
                    <span class="comment-like-count">${comment.likes}</span>
                </div>
                <button class="edit-comment">Edit</button>
                <button class="delete-comment" onclick="deleteComment(${comment.id}, ${postID})">Delete</button>
                <span class="comment-posted">Written on ${comment.posted} by ${comment.author}</span>
            </div>
            <br>
        </section>`
      );
      $('#' + String(postID) + ' .comments-section')[0].append($newCommentSection[0]);
    },
    error: function() {
      alert("Sorry, couldn't post comment at this time!");
    }
  });

  // clear form and stop submit
  $('#' + String(postID) + ' input[name="comment"]')[0].value = "";
  return false;
}

function deleteComment(commentID, entryID) {
  $.post({
    url: '/deletecomment/' + String(commentID) + '/' + String(entryID),
    success: function() {
      $('#' + String(commentID)).remove();
      var $commentCount = $('#' + String(entryID) + ' .comment-count')[0];
      var commentCount = parseInt($commentCount.innerText);
      $commentCount.innerText = commentCount - 1;
    }
  });
}
