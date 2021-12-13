$(document).ready(function(){

    function ajax_login(){
        $.ajax(
            {
                url:'/ajax-login',
                data: $('form').serializeArray(),
                type:'POST',
                success: function(response){
                    console.log(response)
                },
                error:function(error){
                    console.log(response)
                }
            });
    }
    $('#login-form').submit(function(event){
        event.preventDefault();
    });
});