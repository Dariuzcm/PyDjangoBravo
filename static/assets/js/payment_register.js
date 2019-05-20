$(document).ready(function () {
    $("#btn-reg.pay").click(function () { 
        data={
            date: $("#r_fecha").val(),
            emisor: $("#r_emisor").val(),
            receptor: $("#r_receptor").val(),
            cantidad: $("#r_cantidad").val(),
            motivo: $("#r_motivo").val()
        };
        $.ajax({
            type: "post",
            url: "control/PagoRegistar.php",
            data: data,
            beforeSend: function(){
                $("#status").html("<div class='alert alert-light'> <strong>Procesando Solicitud</strong></div>");
            },
            success: function (response) {
                $("#status").html(response);
                
            }
        });
        return false;
    });
});