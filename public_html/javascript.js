$(document).ready(function() {
    $('form').on('submit', function(event) {
        $.ajax({
            data : {
                image_url : $('#urlInput').val(),
            },
            type : 'POST',
            url : 'http://ec2-18-221-131-219.us-east-2.compute.amazonaws.com:5000/search'
        })
        .done(function(data) {
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            }
            else {
                $('#successAlert').text(data.name).show();
                $('#errorAlert').hide();
            }
        });
        event.preventDefault();
    });
});
