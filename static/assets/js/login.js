$(document).ready(()=>{
    $("#btn-login").click(()=>{
        var data={
            user: $("#user").val(),
            pass: $("#pass").val()
        }
        $.ajax({
            type: "post",
            url: "../pages/control/login.php",
            data: data,
            beforeSend: ()=>{
                $('#status').html('<div role="standing" class="alert alert-primary"> Verificando un momento....</div>')},
            success: function (response) {
                $("#status").html(response);
            },
        });
        return false;
    });
    
});
$(document).ajaxComplete(()=>{
    if($('#result').attr("role")=="success"){
        window.location.href="../index.php";
    }
        
});