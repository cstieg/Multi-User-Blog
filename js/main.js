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
        $("#delete-post-dialog").dialog('close');
        alert('Post deleted!');
    }
  })
}

function closeDialog() {
  $('.dialog').dialog('close');
}

function editPost(postID) {

}
