from django.shortcuts import render
from django.http import HttpResponse
from dhCodeAdmin.app.Employees.models import Employee

# Create your views here.
def index(request):
    return render(request,'Employees/Employees.html')

def Destroy(request):
        id=request.POST['id']
        try:
            edit_employe= Employee.objects.get(id=id)
            CompleteName= edit_employe.nombre+' '+edit_employe.apellido
            return HttpResponse('<div class="alert alert-warning">Empleado '+str(id)+' '+CompleteName+': Eliminado Correctamente</div>')
        except ValueError :
            return HttpResponse('<div class="alert alert-danger">Empleado '+CompleteName+': No se pudo Borrar'+ValueError+'</div>')
        

        
def Update(request):
    data=request.POST
    print(data)
    edit_employe = Employee.objects.get(id=data['id'])
    edit_employe.nombre = data['nombre']
    edit_employe.apellido = data['apellido']
    edit_employe.telefono = data['telefono']
    edit_employe.email = data['email']
    edit_employe.fecha_nac = data['fecha_nac']
    edit_employe.fecha_in = data['fecha_in']
    try:
        edit_employe.save()
        return HttpResponse('<div class="alert alert-success">Empleado '+str(edit_employe.id)+': Actualizado Correctamente</div>')
    except ValueError :
        return HttpResponse('<div class="alert alert-danger">Empleado '+str(edit_employe.id)+'-'+edit_employe.nombre+' '+edit_employe.apellido+': No se pudo actualizar'+ValueError+'</div>')
        
def CreateEmploye(request):
    if request.method=='POST':
        employe = request.POST
        print(employe)
        try:
            Employee(
                nombre = employe.get('nombre'),
                apellido = employe.get('apellido'),
                telefono = employe.get('telefono'),
                email = employe.get('email'),
                fecha_nac = employe.get('fecha_nac'),
                fecha_in = employe.get('fecha_in')
                ).save()
            return HttpResponse('<div class="alert alert-success">Registro Realizado Exitosamente</div>')          
        except ValueError:
            print(ValueError)
            return HttpResponse('<div class="alert alert-danger">No se pudo realizar el registro</div>')

def Search(request):
    if request.method == 'POST':
        search= request.POST['search']
        search=str(search)
    #   result= Employee.objects.raw('SELECT * FROM employees_employee WHERE nombre LIKE "%'+search+'%" OR apellido LIKE "%'+search+'%"OR email LIKE "%'+search+'%" OR telefono LIKE "%'+search+'%";')    
        result = Employee.objects.filter(nombre__icontains=str(search)) | Employee.objects.filter(apellido__icontains=str(search)) | Employee.objects.filter(email__icontains=str(search)) | Employee.objects.filter(telefono__icontains=str(search))
        
        if len(result) != 0:
            return HttpResponse(str(TableBuilder(result)))
        else: 
            return HttpResponse('<div class="alert alert-dark"><h4>No Existen registros con esa descripción</h4></div>')
    else:
        return HttpResponse('<div class="alert alert-warning"><h2>Tú no deberias estar haciendo esto</h2></div>')

def TableBuilder(result):
    alt_table='<table class="table table-striped table-bordered first">'
    alt_table+='<thead><tr><th>Folio</th><th>Nombre </th><th>Apellido</th><th>Telefono</th>'
    alt_table+='<th>Email</th><th>Fecha de Nacimiento</th><th>Fecha de integración</th>'
    alt_table+='<th></th></tr></thead><tbody>'    
    downtable='</tbody>'
    downtable+='<tfoot>'
    downtable+='<tr>'
    downtable+='<th>Folio</th>'
    downtable+='<th>Nombre </th>'
    downtable+='<th>Apellido</th>'
    downtable+='<th>Telefono</th>'
    downtable+='<th>Email</th>'
    downtable+='<th>Fecha de Nacimiento</th>'
    downtable+='<th>Fecha de integración</th>'
    downtable+='<th></th></tr> </tfoot> </table>'
    All_table=''
    content=''
    modalDelete=''
    modalEdit=''
    for emp in result:
        content+='<tr><td>'+str(emp.id)+'</td>'
        content+='<td>'+emp.nombre+'</td>'
        content+='<td>'+emp.apellido+'</td>'
        content+='<td>'+emp.telefono+'</td>'
        content+='<td>'+emp.email+'</td>'
        content+='<td>'+str(emp.fecha_nac)+'</td>'
        content+='<td>'+str(emp.fecha_in)+'</td>'
        content+='<td class="row">'
        content+='<button class="btn btn-sm btn-success" data-toggle="modal" data-target="#modal-'+str(emp.id)+'-edit">Editar</button>'
        content+='<button data-toggle="modal" data-target="#modal-delete-'+str(emp.id)+'"class="btn btn-sm btn-danger">'
        content+='    <i class="far fa-trash-alt"></i>'
        content+='</button>'
        content+='</td>'
        content+='</tr>'
        modalDelete+='<!-- Modal -->'
        modalDelete+='<div class="modal fade" id="modal-delete-'+str(emp.id)+'" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        modalDelete+='      <div class="modal-dialog" role="document">'
        modalDelete+='        <div class="modal-content">'
        modalDelete+='          <div class="modal-header">'
        modalDelete+='<h5 class="modal-title" id="exampleModalLabel">Esta seguro de querer ELIMINAR el empleado con folio: '+str(emp.id)+'?</h5>'
        modalDelete+='<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
        modalDelete+='<span aria-hidden="true">&times;</span>'
        modalDelete+='</button>'
        modalDelete+='</div> <div class="modal-body"> <div id="modal-delete-status"></div>'
        modalDelete+='<h6>Despues de Confirmar se eliminará permanentemente.</h6>'
        modalDelete+='</div><div class="modal-footer">'
        modalDelete+='<button  type="button" class="btn btn-light" data-dismiss="modal">Cerrar</button>'
        modalDelete+=' <button id="btn-delete-'+str(emp.id)+'" type="button" class="btn btn-warning">ELIMINAR</button>'
        modalDelete+='</div></div> </div></div>'
        modalDelete+='<script> $("#modal").on("shown.bs.modal", function () {'
        modalDelete+='$("#modal-delete-'+str(emp.id)+'").trigger("focus");   });'
        modalDelete+='$("#btn-delete-'+str(emp.id)+'").click(()=>{ '
        modalDelete+='$.ajax({ type: "post", url: "delete/",data: { id: "'+str(emp.id)+'"},'
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
        modalEdit+='<div class="modal fade" id="modal-'+str(emp.id)+'-edit" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        modalEdit+='<div class="modal-dialog" role="document">'
        modalEdit+='<div class="modal-content">'
        modalEdit+='<div class="modal-header">'
        modalEdit+=' <h5 class="modal-title" id="exampleModalLabel">Editar Registro: '+str(emp.id)+'</h5>'
        modalEdit+='<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
        modalEdit+='<span aria-hidden="true">&times;</span>'
        modalEdit+='</button>'
        modalEdit+='</div>'
        modalEdit+='<div class="modal-body">'
        modalEdit+='<form class="form-control" id="editform">'
        modalEdit+='<div class="form-control">'
        modalEdit+='<div id="modal-status-'+str(emp.id)+'"></div>'
        modalEdit+='<h6 class="card-header">Nombre: <input required name="id" readonly type="text" class="form-control" value="'+str(emp.id)+'"></h6>'
        modalEdit+='<h6 class="card-header">Nombre: <input required name="nombre" id="input-nombre-'+str(emp.id)+'" type="text" class="form-control" value="'+emp.nombre+'"></h6>'
        modalEdit+='<h6 class="card-header">Apellidos: <input required name="apellido" id="input-apellido-'+str(emp.id)+'" type="text" class="form-control"value="'+emp.apellido+'"></h6>'
        modalEdit+='<h6 class="card-header">Telefono: <input required name="telefono" id="input-telefono-'+str(emp.id)+'" type="phone" class="form-control" value="'+emp.telefono+'"></h6>'
        modalEdit+='<h6 class="card-header">Email: <input required name="email" id="input-email-'+str(emp.id)+'" type="email" class="form-control"value="'+emp.email+'" ></h6>'
        modalEdit+='<h6 class="card-header">Fecha de nacimiento: <input required name="fecha_nac" id="input-fecha_nac-'+str(emp.id)+'" type="date" class="form-control" value="'+str(emp.fecha_nac)+'"></h6>'
        modalEdit+='<h6 class="card-header">Fecha de ingreso: <input required name="fecha_in" id="input-fecha_in-'+str(emp.id)+'" type="date" class="form-control" value="'+str(emp.fecha_in)+'"></h6>'
        modalEdit+='</div>'
        modalEdit+='</div>'
        modalEdit+='<div class="modal-footer">'
        modalEdit+='<button id="btn-cancel-'+str(emp.id)+'" type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>'
        modalEdit+='<button id="btn-update-'+str(emp.id)+'" type="button" class="btn btn-primary" disabled >Guardar Cambios</button>'
        modalEdit+='</div></form></div></div></div><script>'
        modalEdit+='$("#modal").on("shown.bs.modal", function () {'
        modalEdit+='$("#modal-'+str(emp.id)+'-edit").trigger("focus")});'
        modalEdit+='$("#input-nombre-'+str(emp.id)+'").change(()=>{'
        modalEdit+='$("#btn-update-'+str(emp.id)+'").removeAttr("disabled");'
        modalEdit+='});'
        modalEdit+='$("#input-apellido-'+str(emp.id)+'").change(()=>{'
        modalEdit+='$("#btn-update-'+str(emp.id)+'").removeAttr("disabled");'
        modalEdit+='});'
        modalEdit+=' $("#input-telefono-'+str(emp.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(emp.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#input-email-'+str(emp.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(emp.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#input-fecha_nac-'+str(emp.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(emp.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#input-fecha_in-'+str(emp.id)+'").change(()=>{'
        modalEdit+='   $("#btn-update-'+str(emp.id)+'").removeAttr("disabled");'
        modalEdit+=' });'
        modalEdit+=' $("#btn-update-'+str(emp.id)+'").click(()=>{ '   
        modalEdit+='   data = $("#editform").serialize();'
        modalEdit+='     $.ajax({'
        modalEdit+='       type: "post",'
        modalEdit+='       url: "update/",'
        modalEdit+='       data: data,'
        modalEdit+=' beforeSend: function(xhr, settings) {'
        modalEdit+='if (!csrfSafeMethod(settings.type) && !this.crossDomain) {'
        modalEdit+='    xhr.setRequestHeader("X-CSRFToken", csrftoken);'
        modalEdit+='}'
        modalEdit+='       $("#modal-status-'+str(emp.id)+'").html("<div class=\'alert alert-light\'>Realizando Cambios</div>");'
        modalEdit+='       },'
        modalEdit+='       success: (response)=> {'
        modalEdit+='       $("#modal-status-'+str(emp.id)+'").html(response);'
        modalEdit+='         location.reload();}'
        modalEdit+='     });'
        modalEdit+='   });'
        modalEdit+='   $("#btn-cancel-'+str(emp.id)+'").click(()=>{'
        modalEdit+='     $("#btn-update-'+str(emp.id)+'").attr("disabled","disabled");'
        modalEdit+='   });'
        modalEdit+=' </script>'

        if not content:
            All_table=alt_table+'<tr><td>No existen Registros</td></tr>'+downtable
        else:
            All_table=alt_table+content+downtable+modalEdit+modalDelete
        return All_table