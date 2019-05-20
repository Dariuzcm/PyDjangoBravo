$(document).ready(()=>{
    $("#btn-Reg").click(()=>{
        var data={ 
            usuario : $("#username").val(),
            contra: $("#pass1").val()
        };
        $.ajax({
            type: "post",
            url: "../pages/control/registrar.php",
            data: data,
            beforeSend: function(){
                $("#status").html('<div class="alert-alert-primary" role="primary">Procesando, espere un momento...</div>');
            },
            success: function (response) {
                    $("#status").html(response);
            }
           
        });
        return false;

    });
});