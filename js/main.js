function verifyDeletePost(postID) {
  $('#delete-post-dialog').dialog();
  $('#delete-post-dialog [name=delete]').attr('onclick', 'deletePost(' + String(postID) + ')');
}


function deletePost(postID) {
  $.ajax({
    type : 'POST',
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
  $.ajax({
    type : 'POST',
    url : '/likepost/' + String(postID),
    success: function() {
      // toggle to unlike
      $('#' + postID + ' .like-button').text = 'Unlike';

      // change onclick to unlike function
      oldFunc = $('#' + postID + ' .like-button').attr('onclick');
      newFunc = oldFunc.replace('like', 'unlike');
      $('#' + postID + ' .like-button').attr('onclick', newFunc);

      // increment like-count
      likeCount = Integer($('#' + postID + ' .like-count').text);
      $('#' + postID + ' .like-count').text = likeCount + 1;
    }
  });
}

function unlikePost(postID) {
  $.ajax({
    type : 'POST',
    url : '/unlikepost/' + String(postID),
    success: function() {
      // toggle to unlike
      $('#' + postID + ' .like-button').text = 'Like';

      // increment like-count
      likeCount = Integer($('#' + postID + ' .like-count').text);
      $('#' + postID + ' .like-count').text = likeCount - 1;
    }
  });
}
