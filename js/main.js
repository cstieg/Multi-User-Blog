var WAITING_FOR_AJAX = false;

// confirmation dialog box on deletion
function verifyDeletePost(entryID) {
  $('#delete-post-dialog').dialog();
  $('#delete-post-dialog [name=delete]').attr('onclick', 'deletePost(' + String(entryID) + ')');
}

// make ajax call to server to delete entry, and on success, remove entry
// without refreshing page
function deletePost(entryID) {
  $.post({
    url : '/deletepost/' + String(entryID),
    success: function() {
        $('#' + String(entryID)).remove();
        $('#delete-post-dialog').dialog('close');
        alert('Post deleted!');
    }
  });
}

// make ajax call to server to like entry, and on success, toggle like button
// to unlike and increment like count without refreshing page
function f_likePost(entryID) {
  if (WAITING_FOR_AJAX) {
    return;
  }
  WAITING_FOR_AJAX = true;
  var $likeButton = $('#' + entryID + ' .like-button');
  $.post({
    url : '/likepost/' + String(entryID),
    success: function() {
      var $likeCount = $('#' + entryID + ' .like-count');
      // toggle to unlike
      $likeButton.text('👍 Unlike');

      // change onclick to unlike function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('f_like', 'f_unlike');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      var likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount + 1);
      WAITING_FOR_AJAX = false;
    },
    error: function() {
      alert("Not allowed to like!");
      WAITING_FOR_AJAX = false;
    }
  });
}

// make ajax call to server to unlike entry, and on success, toggle unlike
// button to like and decrement like count wihout refreshing page
function f_unlikePost(entryID) {
  if (WAITING_FOR_AJAX) {
    return;
  }
  WAITING_FOR_AJAX = true;
  var $likeButton = $('#' + entryID + ' .like-button');
  $.post({
    url: '/unlikepost/' + String(entryID),
    success: function() {
      var $likeCount = $('#' + entryID + ' .like-count');

      // toggle to unlike
      $likeButton.text('👍 Like');

      // change onclick to like function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('f_unlike', 'f_like');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      var likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount - 1);
      WAITING_FOR_AJAX = false;
    },
    error: function() {
      alert("Not allowed to unlike!");
      WAITING_FOR_AJAX = false;
    }
  });
}

// toggle comment section with button
function toggleComment(entryID) {
  var $commentsSection = $('#' + entryID + ' .comments-section');
  if ($commentsSection.hasClass('no-display')) {
    $commentsSection.removeClass('no-display');
    $commentsSection.find('textarea')[0].focus();
    // make textarea submit on enter
    $commentsSection.find('textarea').keypress(function(e) {
      if(e.which == 13) {
        $commentsSection.find('form').submit();
        return false;
      }
    });
  }
  else {
    $commentsSection.addClass('no-display');
  }
}

// make ajax call to server to add comment and immediately add to html without refreshing
function addComment(entryID, username) {
  var $newCommentTextarea = $('#' + String(entryID) + ' textarea')[0];
  var commentText = $newCommentTextarea.value;
  $.post({
    url:  '/addcomment/' + String(entryID),
    data: {'comment': commentText},
    success: function(response) {
      // create new comment section without refreshing
      var comment = JSON.parse(response);
      var $newCommentSection = commentSectionHTML(comment, entryID, username);
      $('#' + String(entryID) + ' .comments-section')[0].append($newCommentSection[0]);
      var $commentCount = $('#' + String(entryID) + ' .comment-count')[0];
      var commentCount = parseInt($commentCount.innerText);
      $commentCount.innerText = commentCount + 1;
    },
    error: function() {
      alert("Sorry, couldn't post comment at this time!");
    }
  });

  // clear form and stop submit
  $newCommentTextarea.value = '';
  return false;
}

// make ajax call to server to delete comment and immediately remove from html
// without refreshing
function deleteComment(commentID) {
  $.post({
    url: '/deletecomment/' + String(commentID),
    success: function() {
      $commentToRemove = $('#' + String(commentID));
      $parentEntry = $commentToRemove.closest('article');
      $commentToRemove.remove();
      var $commentCount = $parentEntry.find('.comment-count')[0];
      var commentCount = parseInt($commentCount.innerText);
      $commentCount.innerText = commentCount - 1;
    }
  });
}

// open dialog box to edit comment
function editCommentInput(commentID) {
  var $commentText = $('#' + commentID + ' .comment-text')[0];
  var commentText = $commentText.innerText;
  var onSubmitFunction = function() {
    return editComment(commentID);
  }
  $('#edit-comment-dialog form').on('submit', onSubmitFunction);
  $('#edit-comment-dialog [name=comment]').attr('value', commentText);
  $('#edit-comment-dialog').dialog();
}

// make ajax call to server to update comment and immediately update HTML
function editComment(commentID) {
  var commentTextField = $('#edit-comment-dialog [name=comment]');
  var commentText = commentTextField[0].value;
  $.post({
    url: '/editcomment/' + String(commentID),
    data: {'comment': commentText},
    success: function() {
      $('#' + commentID + ' .comment-text')[0].innerText = commentText;
    },
    error: function() {
      alert('Could not edit comment!');
    }
  });
  closeDialog(commentTextField);
  return false;
}

// template to create a new comment section after addComment without refreshing
function commentSectionHTML(comment, username) {
  return $.parseHTML(
  `<section class="comment" id="${comment.id}">
        <p class="comment-text">
            ${comment.comment}
        </p>
        <div class="comment-footer">
          <div class="comment-likes">
            <span class="like-comment-button"
            <span class="like-comment-label">👍 Likes: </span>
            <span class="like-comment-count">0</span>
          </div>
          <button class="edit-comment" onclick="editCommentInput(${comment.id})">Edit</button>
          <button class="delete-comment" onclick="deleteComment(${comment.id})">Delete</button>
          <span class="comment-posted">Written on ${comment.posted} by ${comment.author}</span>
        </div>
        <br>
    </section>`
  );
}

// make ajax call to server to like comment and increment comment like count
function f_likeComment(commentID) {
  if (WAITING_FOR_AJAX) {
    return;
  }
  WAITING_FOR_AJAX = true;
  $.post({
    url : '/likecomment/' + String(commentID),
    success: function() {
      var $likeButton = $('#' + commentID + ' .like-comment-button');
      var $likeCount = $('#' + commentID + ' .like-comment-count');
      // toggle to unlike
      $likeButton.text('👍 Unlike');

      // change onclick to unlike function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('f_like', 'f_unlike');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      var likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount + 1);
      WAITING_FOR_AJAX = false;
    },
    error: function() {
      alert('Not allowed to like!');
      WAITING_FOR_AJAX = false;
    }
  });
}

// make ajax call to server to unlike comment and decrement comment like count
function f_unlikeComment(commentID) {
  if (WAITING_FOR_AJAX) {
    return;
  }
  WAITING_FOR_AJAX = true;
  $.post({
    url: '/unlikecomment/' + String(commentID),
    success: function() {
      var $likeButton = $('#' + commentID + ' .like-comment-button');
      var $likeCount = $('#' + commentID + ' .like-comment-count');

      // toggle to unlike
      $likeButton.text('👍 Like');

      // change onclick to like function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('f_unlike', 'f_like');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      var likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount - 1);
      WAITING_FOR_AJAX = false;
    },
    error: function() {
      alert("Not allowed to unlike!");
      WAITING_FOR_AJAX = false;
    }
  });
}

// close dialog box opened by edit comment dialog or delete post dialog
function closeDialog(dialogButton) {
  var dialogDiv = $(dialogButton).closest('div');
  dialogDiv.dialog('close');
}
