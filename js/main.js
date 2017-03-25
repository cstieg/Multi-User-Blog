function verifyDeletePost(entryID) {
  $('#delete-post-dialog').dialog();
  $('#delete-post-dialog [name=delete]').attr('onclick', 'deletePost(' + String(entryID) + ')');
}

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

function closeDialog(dialogButton) {
  var dialogDiv = $(dialogButton).closest('div');
  dialogDiv.dialog('close');
}

function likePost(entryID) {
  $.post({
    url : '/likepost/' + String(entryID),
    success: function() {
      var $likeButton = $('#' + entryID + ' .like-button');
      var $likeCount = $('#' + entryID + ' .like-count');
      // toggle to unlike
      $likeButton.text('👍 Unlike');

      // change onclick to unlike function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('like', 'unlike');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount + 1);
    },
    error: function() {
      alert("Not allowed to like!");
    }
  });
}

function unlikePost(entryID) {
  $.post({
    url: '/unlikepost/' + String(entryID),
    success: function() {
      var $likeButton = $('#' + entryID + ' .like-button');
      var $likeCount = $('#' + entryID + ' .like-count');

      // toggle to unlike
      $likeButton.text('👍 Like');

      // change onclick to like function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('unlike', 'like');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount - 1);
    },
    error: function() {
      alert("Not allowed to unlike!");
    }
  });
}

function toggleComment(entryID) {
  var $commentsSection = $('#' + entryID + ' .comments-section');
  if ($commentsSection.hasClass('no-display')) {
    $commentsSection.removeClass('no-display');
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
    },
    error: function() {
      alert("Sorry, couldn't post comment at this time!");
    }
  });

  // clear form and stop submit
  $newCommentTextarea.value = '';
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

function editCommentInput(commentID, entryID) {
  var $commentText = $('#' + commentID + ' .comment-text')[0];
  var commentText = $commentText.innerText;
  var onSubmitFunction = function() {
    return editComment(commentID, entryID);
  }
  $('#edit-comment-dialog form').on('submit', onSubmitFunction);
  $('#edit-comment-dialog [name=comment]').attr('value', commentText);
  $('#edit-comment-dialog').dialog();
}

function editComment(commentID, entryID) {
  var commentTextField = $('#edit-comment-dialog [name=comment]');
  var commentText = commentTextField[0].value;
  $.post({
    url: '/editcomment/' + String(commentID) + '/' + String(entryID),
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

function commentSectionHTML(comment, entryID, username) {
  var commentHTML =
  `<section class="comment" id="${comment.id}">
        <p class="comment-text">
            ${comment.comment}
        </p>
        <div class="comment-footer">
            <div class="comment-likes">
                <span class="like-comment-button"`;
    if (comment.author != username) {
      commentHTML += ` onclick="`;
      if (comment.liked) {
        commentHTML += `unlikeComment`;
      }
      else {
        commentHTML += `likeComment`;
      }
      commentHTML += `({{comment.id}}, {{entry.id}})">`;
    }
    commentHTML += `👍</span>
                <span class="like-comment-count">${comment.likeCount}</span>
            </div>
            <button class="edit-comment" onclick="editCommentInput(${comment.id}, ${entryID})">Edit</button>
            <button class="delete-comment" onclick="deleteComment(${comment.id}, ${entryID})">Delete</button>
            <span class="comment-posted">Written on ${comment.posted} by ${comment.author}</span>
        </div>
        <br>
    </section>`;

    return $.parseHTML(commentHTML);
}

function likeComment(commentID, entryID) {
  $.post({
    url : '/likecomment/' + String(commentID) + '/' + String(entryID),
    success: function() {
      var $likeButton = $('#' + commentID + ' .like-comment-button');
      var $likeCount = $('#' + commentID + ' .like-comment-count');
      // toggle to unlike
      $likeButton.text('👍 Unlike');

      // change onclick to unlike function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('like', 'unlike');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount + 1);
    },
    error: function() {
      alert("Not allowed to like!");
    }
  });
}

function unlikeComment(commentID, entryID) {
  $.post({
    url: '/unlikecomment/' + String(commentID) + '/' + String(entryID),
    success: function() {
      var $likeButton = $('#' + commentID + ' .like-comment-button');
      var $likeCount = $('#' + commentID + ' .like-comment-count');

      // toggle to unlike
      $likeButton.text('👍 Like');

      // change onclick to like function
      oldFunc = $likeButton.attr('onclick');
      newFunc = oldFunc.replace('unlike', 'like');
      $likeButton.attr('onclick', newFunc);

      // increment like-count
      likeCount = parseInt($likeCount.text());
      $likeCount.text(likeCount - 1);
    },
    error: function() {
      alert("Not allowed to unlike!");
    }
  });
}
