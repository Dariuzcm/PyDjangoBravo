from django.shortcuts import render
from django.http import HttpResponse
from dhCodeAdmin.app.Payments.models import Payment

# Create your views here.
def index(request):
    return render(request,'Payments/Payments.html')

def Destroy(request):
        id=request.POST['id']
        try:
            edit_payment= Payment.objects.get(id=id)
            motivo= edit_payment.motivo
            edit_payment.delete()
            
        except ValueError :
            return HttpResponse('<div class="alert alert-danger">Pago con motivo de: '+motivo+', NO se pudo Borrar'+ValueError+'</div>')
        
        return HttpResponse('<div class="alert alert-warning">Pago con motivo de: '+motivo+', Eliminado Correctamente</div>')
        

        
def Update(request):
    data=request.POST
    edit_payment = Payment.objects.get(id=data['id'])
    edit_payment.emisor = data['emisor']
    edit_payment.receptor = data['receptor']
    edit_payment.motivo = data['motivo']
    edit_payment.cantidad = data['cantidad']
    edit_payment.fecha = data['fecha']
    try:
        edit_payment.save()
        return HttpResponse('<div class="alert alert-success">Pago '+str(edit_payment.id)+' con motivo de: '+edit_payment.motivo+', Actualizado Correctamente</div>')
    except ValueError :
        return HttpResponse('<div class="alert alert-danger">Pago '+str(edit_payment.id)+' con motivo de: '+edit_payment.motivo+', No se pudo actualizar'+ValueError+'</div>')
        
def Create(request):
    if request.method=='POST':
        payment = request.POST
        try:
            Payment(
                emisor = payment.get('emisor'),
                receptor = payment.get('receptor'),
                cantidad = payment.get('cantidad'),
                motivo = payment.get('motivo'),
                fecha = payment.get('fecha')
                ).save()
            return HttpResponse('<div class="alert alert-success">Registro Realizado Exitosamente</div>')          
        except ValueError:
            return HttpResponse('<div class="alert alert-danger">No se pudo realizar el registro</div>')

def Search(request):
    if request.method == 'POST':
        search= request.POST['search']
        search=str(search)
    #   result= paymloyee.objects.raw('SELECT * FROM paymloyees_paymloyee WHERE nombre LIKE "%'+search+'%" OR apellido LIKE "%'+search+'%"OR email LIKE "%'+search+'%" OR telefono LIKE "%'+search+'%";')    
        result = Payment.objects.filter(motivo__icontains=str(search)) | Payment.objects.filter(receptor__icontains=str(search)) | Payment.objects.filter(emisor__icontains=str(search)) | Fecha.objects.filter(fecha__icontains=str(search))
        
        if len(result) != 0:
            return HttpResponse(str(TableBuilder(result)))
        else: 
            return HttpResponse('<div class="alert alert-dark"><h4>No Existen registros con esa descripción</h4></div>')
    else:
        return HttpResponse('<div class="alert alert-warning"><h2>Tú no deberias estar haciendo esto</h2></div>')

def TableBuilder(result):
    alt_table='<table class="table table-striped table-bordered first">'
    alt_table+='<thead><tr><th>Folio</th><th>Nombre de emisor </th><th>Nombre de receptor</th><th>Cantidad</th>'
    alt_table+='<th>Motivo</th><th>Fecha</th>'
    alt_table+='<th></th></tr></thead><tbody>'    
    downtable='</tbody>'
    downtable+='<tfoot>'
    downtable+='<tr>'
    downtable+='<th>Folio</th>'
    downtable+='<th>Nombre de emisor </th>'
    downtable+='<th>Nombre de receptor</th>'
    downtable+='<th>Cantidad</th>'
    downtable+='<th>Motivo</th>'
    downtable+='<th>Fecha</th>'
    downtable+='<th></th></tr> </tfoot> </table>'
    All_table=''
    content=''
    modalDelete=''
    modalEdit=''
    for paym in result:
        content+='<tr><td>'+str(paym.id)+'</td>'
        content+='<td>'+paym.emisor+'</td>'
        content+='<td>'+paym.receptor+'</td>'
        content+='<td>'+paym.cantidad+'</td>'
        content+='<td>'+paym.motivo+'</td>'
        content+='<td>'+str(paym.fecha)+'</td>'
        content+='<td class="row">'
        content+='<button class="btn btn-sm btn-success" data-toggle="modal" data-target="#modal-'+str(paym.id)+'-edit">Editar</button>'
        content+='<button data-toggle="modal" data-target="#modal-delete-'+str(paym.id)+'"class="btn btn-sm btn-danger">'
        content+='    <i class="far fa-trash-alt"></i>'
        content+='</button>'
        content+='</td>'
        content+='</tr>'
        modalDelete+='<!-- Modal -->'
        modalDelete+='<div class="modal fade" id="modal-delete-'+str(paym.id)+'" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        modalDelete+='      <div class="modal-dialog" role="document">'
        modalDelete+='        <div class="modal-content">'
        modalDelete+='          <div class="modal-header">'
        modalDelete+='<h5 class="modal-title" id="exampleModalLabel">Esta seguro de querer ELIMINAR el pago con folio: '+str(paym.id)+'?</h5>'
        modalDelete+='<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
        modalDelete+='<span aria-hidden="true">&times;</span>'
        modalDelete+='</button>'
        modalDelete+='</div> <div class="modal-body"> <div id="modal-delete-status"></div>'
        modalDelete+='<h6>Despues de Confirmar se eliminará permanentemente.</h6>'
        modalDelete+='</div><div class="modal-footer">'
        modalDelete+='<button  type="button" class="btn btn-light" data-dismiss="modal">Cerrar</button>'
        modalDelete+=' <button id="btn-delete-'+str(paym.id)+'" type="button" class="btn btn-warning">ELIMINAR</button>'
        modalDelete+='</div></div> </div></div>'
        modalDelete+='<script> $("#modal").on("shown.bs.modal", function () {'
        modalDelete+='$("#modal-delete-'+str(paym.id)+'").trigger("focus");   });'
        modalDelete+='$("#btn-delete-'+str(paym.id)+'").click(()=>{ '

        modalDelete+='$.ajax({ type: "post", url: "delete/",data: { id: "'+str(paym.id)+'"},'
        modalDelete+='beforeSend: function(xhr, settings) {'
        modalDelete+='if (!csrfSafeMethod(settings.type) && !this.crossDomain) {'
        modalDelete+='    xhr.setRequestHeader("X-CSRFToken", csrftoken);'
        modalDelete+='}'
        modalDelete+='$("#modal-delete-status").html("<div class=\'alert alert-light\'>Execute Deleting</div>"); },'
        modalDelete+='success: function (response) {$("#modal-delete-status").html(response); location.reload(); },' 
        modalDelete+='error:(e)=>{ $("#modal-delete-status").html(e);}'
        modalDelete+='});'
        modalDelete+='return false; });</script>'

        modalEdit+='<!-- Modal -->'
        modalEdit+='<div class="modal fade" id="modal-'+str(paym.id)+'-edit" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        modalEdit+='<div class="modal-dialog" role="document">'
        modalEdit+='<div class="modal-content">'
        modalEdit+='<div class="modal-header">'
        modalEdit+=' <h5 class="modal-title" id="exampleModalLabel">Editar Registro: '+str(paym.id)+'</h5>'
        modalEdit+='<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
        modalEdit+='<span aria-hidden="true">&times;</span>'
        modalEdit+='</button>'
        modalEdit+='</div>'
        modalEdit+='<div class="modal-body">'
        modalEdit+='<form class="form-control" id="editform">'
        modalEdit+='<div class="form-control">'
        modalEdit+='<div id="modal-status-'+str(paym.id)+'"></div>'
        modalEdit+='<h6 class="card-header">Id: <input required name="id" readonly type="text" class="form-control" value="'+str(paym.id)+'"></h6>'
        modalEdit+='<h6 class="card-header">Nombre: <input required name="emisor" id="input-nombre-'+str(paym.id)+'" type="text" class="form-control" value="'+paym.emisor+'"></h6>'
        modalEdit+='<h6 class="card-header">Apellidos: <input required name="receptor" id="input-apellido-'+str(paym.id)+'" type="text" class="form-control"value="'+paym.receptor+'"></h6>'
        modalEdit+='<h6 class="card-header">Telefono: <input required name="cantidad" id="input-telefono-'+str(paym.id)+'" type="number" class="form-control" value="'+paym.cantidad+'"></h6>'
        modalEdit+='<h6 class="card-header">Email: <input required name="motivo" id="input-email-'+str(paym.id)+'" type="text" class="form-control"value="'+paym.motivo+'" ></h6>'
        modalEdit+='<h6 class="card-header">Fecha de nacimiento: <input required name="fecha" id="input-fecha_nac-'+str(paym.id)+'" type="date" class="form-control" value="'+str(paym.fecha)+'"></h6>'
        modalEdit+='</div>'
        modalEdit+='</div>'
        modalEdit+='<div class="modal-footer">'
        modalEdit+='<button id="btn-cancel-'+str(paym.id)+'" type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>'
        modalEdit+='<button id="btn-update-'+str(paym.id)+'" type="button" class="btn btn-primary" disabled >Guardar Cambios</button>'
        modalEdit+='</div></form></div></div></div><script>'
        modalEdit+='$("#modal").on("shown.bs.modal", function () {'
        modalEdit+='$("#modal-'+str(paym.id)+'-edit").trigger("focus")});'
        modalEdit+='$("#input-nombre-'+str(paym.id)+'").change(()=>{'
        modalEdit+='$("#btn-update-'+str(paym.id)+'").removeAttr("disabled");'
        modalEdit+='});'
        modalEdit+='$("#input-apellido-'+str(paym.id)+'").change(()=>{'
        modalEdit+='$("#btn-update-'+str(paym.id)+'").removeAttr("disabled");'
        modalEdit+='});'
        modalEdit+=' $("#input-telefono-'+str(paym.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(paym.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#input-email-'+str(paym.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(paym.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#input-fecha_nac-'+str(paym.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(paym.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#input-fecha_in-'+str(paym.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(paym.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#btn-update-'+str(paym.id)+'").click(()=>{ '   
        modalEdit+='   data = $("#editform").serialize();'
        modalEdit+='     $.ajax({'
        modalEdit+='       type: "post",'
        modalEdit+='       url: "update/",'
        modalEdit+='       data: data,'
        modalEdit+=' beforeSend: function(xhr, settings) {'
        modalEdit+='if (!csrfSafeMethod(settings.type) && !this.crossDomain) {'
        modalEdit+='    xhr.setRequestHeader("X-CSRFToken", csrftoken);'
        modalEdit+='}'
        modalEdit+='       $("#modal-status-'+str(paym.id)+'").html("<div class=\'alert alert-light\'>Realizando Cambios</div>");'
        modalEdit+='       },'
        modalEdit+='       success: (response)=> {'
        modalEdit+='       $("#modal-status-'+str(paym.id)+'").html(response);'
        modalEdit+='         location.reload();}'
        modalEdit+='     });'
        modalEdit+='   });'
        modalEdit+='   $("#btn-cancel-'+str(paym.id)+'").click(()=>{'
        modalEdit+='     $("#btn-update-'+str(paym.id)+'").attr("disabled","disabled");'
        modalEdit+='   });'
        modalEdit+=' </script>'

        All_table=alt_table+content+downtable+modalEdit+modalDelete
        return All_table