from django.shortcuts import render
from django.http import HttpResponse
from dhCodeAdmin.app.Projects.models import Project
# Create your views here.
def index (request):
    return render(request,'Projects/Projects.html')

def Destroy(request):
    id=request.POST['id']
    try:
        edit_project= Project.objects.get(id=id)
        Proyect_name= edit_project.proyect_name
        edit_project.delete()
        return HttpResponse('<div class="alert alert-warning">Proyecto <strong>'+Proyect_name+'</strong>: Eliminado Correctamente</div>')
    except ValueError :
        return HttpResponse('<div class="alert alert-danger">Proyecto '+Proyect_name+': No se pudo Borrar'+ValueError+'</div>')
def Update(request):
    data=request.POST
    edit_project = Project.objects.get(id=data['id'])
    edit_project.proyect_name = data['proyect_name']
    edit_project.begin_date = data['begin_date']
    edit_project.end_date = data['end_date']
    edit_project.manager_name = data['manager_name']
    edit_project.client_name = data['client_name']
    try:
        edit_project.save()
        return HttpResponse('<div class="alert alert-success">Proyecto '+str(edit_project.id)+': Actualizado Correctamente</div>')
    except ValueError :
        return HttpResponse('<div class="alert alert-danger">Proyecto '+str(edit_project.id)+'-'+edit_project.proyect_name+': No se pudo actualizar'+ValueError+'</div>')
def Create(request):
    if request.method=='POST':
        proyect = request.POST
        try:
            Project(
                proyect_name = proyect.get('proyect_name'),
                begin_date = proyect.get('begin_date'),
                end_date = proyect.get('end_date'),
                manager_name = proyect.get('manager_name'),
                client_name = proyect.get('client_name')
                ).save()
            return HttpResponse('<div class="alert alert-success">Registro Realizado Exitosamente</div>')          
        except ValueError:
            return HttpResponse('<div class="alert alert-danger">No se pudo realizar el registro</div>')
def Search(request):
    if request.method == 'POST':
        search= request.POST['search']
        search=str(search)
        result = Project.objects.filter(proyect_name__icontains=str(search)) | Project.objects.filter(id__icontains=str(search)) 
        
        if len(result) != 0:
            return HttpResponse(str(TableBuilder(result)))
        else: 
            return HttpResponse('<div class="alert alert-dark"><h4>No Existen registros con esa descripción</h4></div>')
    else:
        return HttpResponse('<div class="alert alert-warning"><h2>Tú no deberias estar haciendo esto</h2></div>')
def TableBuilder(result):
    modalEdit=''
    modalDelete=''
    altable='<table class="table table-striped table-bordered first">'
    altable+='           <thead>'
    altable+='           <tr>'
    altable+='                       <th>Folio</th>'
    altable+='                       <th>Nombre del Proyecto</th>'
    altable+='                       <th>Fecha de Inicio</th>'
    altable+='                       <th>Fecha de Finalización</th>'
    altable+='                       <th>Nombre de Lider</th>'
    altable+='                       <th>Nombre de cliente</th>'
    altable+='                       <th></th>'
    altable+='                   </tr>'
    altable+='               </thead>'
    altable+='               <tbody>'
    downtable='</tbody>'
    downtable+='                      <tfoot>'
    downtable+='                 <tr>'
    downtable+='                 <th>Folio</th>'
    downtable+='                 <th>Nombre del Proyecto</th>'
    downtable+='                 <th>Fecha de Inicio</th>'
    downtable+='                 <th>Fecha de Finalización</th>'
    downtable+='                 <th>Nombre de Lider</th>'
    downtable+='                 <th>Nombre de cliente</th>'
    downtable+='                 <th></th>'
    downtable+='             </tr>'
    downtable+='             </tfoot>'
    downtable+='         </table>'
    content=''
    Alltable=altable
    modalEdit=''
    modalDelete=''
    for proyect in result:
        content+='<tr>'
        content+='    <td>'+str(proyect.id)+'</td>'
        content+='    <td>'+proyect.proyect_name+'</td>'
        content+='    <td>'+str(proyect.begin_date)+'</td>'
        content+='    <td>'+str(proyect.end_date)+'</td>'
        content+='   <td>'+proyect.manager_name+'</td>'
        content+='    <td>'+proyect.client_name+'</td>'
        content+='   <td>'
        content+='        <button class="btn btn-sm btn-success" data-toggle="modal" data-target="#modal-'+str(proyect.id)+'-edit">Editar</button>'
        content+='        <button data-toggle="modal" data-target="#modal-delete-'+str(proyect.id)+'"class="btn btn-sm btn-danger">'
        content+='            <i class="far fa-trash-alt"></i>'
        content+='        </button>'
        content+='    </td>'
        content+='    </tr>'

        modalDelete+='<!-- Modal -->'
        modalDelete+='<div class="modal fade" id="modal-delete-'+str(proyect.id)+'" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        modalDelete+='  <div class="modal-dialog" role="document">'
        modalDelete+='    <div class="modal-content">'
        modalDelete+='      <div class="modal-header">'
        modalDelete+='        <h5 class="modal-title" id="exampleModalLabel">Esta seguro de querer ELIMINAR el proyecto con folio: '+str(proyect.id)+'?</h5>'
        modalDelete+='        <button type="button" class="close" data-dismiss="modal" aria-label="Close">'
        modalDelete+='          <span aria-hidden="true">&times;</span>'
        modalDelete+='        </button>'
        modalDelete+='      </div>'
        modalDelete+='      <div class="modal-body">'
        modalDelete+='        <div id="modal-delete-status"></div>'
        modalDelete+='        <h6>Despues de Confirmar se eliminará permanentemente.</h6>'
        modalDelete+='      </div>'
        modalDelete+='      <div class="modal-footer">'
        modalDelete+='        <button  type="button" class="btn btn-light" data-dismiss="modal">Cerrar</button>'
        modalDelete+='        <button id="btn-delete-'+str(proyect.id)+'" type="button" class="btn btn-warning">ELIMINAR</button>'
        modalDelete+='      </div>'
        modalDelete+='    </div>'
        modalDelete+='  </div>'
        modalDelete+='</div><script>'
        modalDelete+='$("#modal").on("shown.bs.modal", function () {'
        modalDelete+='    $("#modal-delete-'+str(proyect.id)+'").trigger("focus");'
        modalDelete+='  });'

        modalDelete+='  $("#btn-delete-'+str(proyect.id)+'").click(()=>{'
        modalDelete+='      $.ajax({'
        modalDelete+='        type: "post",'
        modalDelete+='        url: "delete/",'
        modalDelete+='        data: { id: "'+str(proyect.id)+'"},'
        modalDelete+='        beforeSend:(xhr, settings)=>{'
        modalDelete+='      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {'
        modalDelete+='    xhr.setRequestHeader("X-CSRFToken", csrftoken);'
        modalDelete+='}'
        modalDelete+='          $("#modal-delete-status").html("<div class=\'alert alert-light\'>Excecute Deleting</div>");'
        modalDelete+='        },'
        modalDelete+='        success: function (response) {'
        modalDelete+='          $("#modal-delete-status").html(response);'
        modalDelete+='          location.reload();'
        modalDelete+='        }'
        modalDelete+='      });'
        modalDelete+='      return false;'
        modalDelete+='  });'
        modalDelete+='</script>'

        modalEdit+='<!-- Modal -->'
        modalEdit+='<div class="modal fade" id="modal-'+str(proyect.id)+'-edit" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        modalEdit+='  <div class="modal-dialog" role="document">'
        modalEdit+='    <div class="modal-content">'
        modalEdit+='      <div class="modal-header">'
        modalEdit+='        <h5 class="modal-title" id="exampleModalLabel">Editar Registro: '+str(proyect.id)+'</h5>'
        modalEdit+='        <button type="button" class="close" data-dismiss="modal" aria-label="Close">'
        modalEdit+='          <span aria-hidden="true">&times;</span>'
        modalEdit+='        </button>'
        modalEdit+='      </div>'
        modalEdit+='      <div class="modal-body">'
        modalEdit+='        <div class="form-control">'
        modalEdit+='        <div id="modal-status-'+str(proyect.id)+'"></div>'
        modalEdit+='        <form id="modalForm-'+str(proyect.id)+'">'
        modalEdit+='        <h6 class="card-header">Fecha: <input required name="id" id="input-id-'+str(proyect.id)+'"type="text" readonly class="form-control" value="'+str(proyect.id)+'"></h6>             '       
        modalEdit+='        <h6 class="card-header">Fecha: <input required name="proyect_name" id="input-proyect_name-'+str(proyect.id)+'"type="text" class="form-control" value="'+proyect.proyect_name+'"></h6>'
        modalEdit+='        <h6 class="card-header">Emisor: <input required name="begin_date"  id="input-begin_date-'+str(proyect.id)+'" type="date" class="form-control"value="'+str(proyect.begin_date)+'"></h6>'
        modalEdit+='        <h6 class="card-header">Receptor: <input required name="end_date" id="input-end_date-'+str(proyect.id)+'" type="date" class="form-control" value="'+str(proyect.end_date)+'"></h6>'
        modalEdit+='        <h6 class="card-header">Cantidad: <input required name="manager_name" id="input-manager_name-'+str(proyect.id)+'" type="text" class="form-control"value="'+proyect.manager_name+'" ></h6>'
        modalEdit+='        <h6 class="card-header">Motivo: <input required name="client_name" id="input-client_name-'+str(proyect.id)+'" type="text" class="form-control" value="'+proyect.client_name+'"></h6>'
        modalEdit+='             </div>'
        modalEdit+='      </div>'
        modalEdit+='      <div class="modal-footer">'
        modalEdit+='        <button id="btn-cancel-'+str(proyect.id)+'" type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>'
        modalEdit+='        <button id="btn-update-'+str(proyect.id)+'" type="button" class="btn btn-primary" disabled >Guardar Cambios</button>'
        modalEdit+='      </div>'
        modalEdit+='    </div>'
        modalEdit+='  </div>'
        modalEdit+='</div><script>'
        modalEdit+='    $("#modal").on("shown.bs.modal", function () {'
        modalEdit+='    $("#modal-'+str(proyect.id)+'-edit").trigger("focus")'
        modalEdit+='  });'
        modalEdit+='  $("#input-proyect_name-'+str(proyect.id)+'").change(()=>{'
        modalEdit+='    $("#btn-update-'+str(proyect.id)+'").removeAttr("disabled");'
        modalEdit+='  });'
        modalEdit+='  $("#input-begin_date-'+str(proyect.id)+'").change(()=>{'
        modalEdit+='    $("#btn-update-'+str(proyect.id)+'").removeAttr("disabled");'
        modalEdit+='  });'
        modalEdit+='  $("#input-end_date-'+str(proyect.id)+'").change(()=>{'
        modalEdit+='    $("#btn-update-'+str(proyect.id)+'").removeAttr("disabled");'
        modalEdit+='  });'
        modalEdit+='  $("#input-manager_name-'+str(proyect.id)+'").change(()=>{'
        modalEdit+='    $("#btn-update-'+str(proyect.id)+'").removeAttr("disabled");'
        modalEdit+='  });'
        modalEdit+='  $("#input-client_name-'+str(proyect.id)+'").change(()=>{'
        modalEdit+='    $("#btn-update-'+str(proyect.id)+'").removeAttr("disabled");'
        modalEdit+='  });'
        modalEdit+='  $("#btn-update-'+str(proyect.id)+'").click(()=>{    '
        modalEdit+='      data= $("#modalForm-'+str(proyect.id)+'").serialize();'
        modalEdit+='    $.ajax({'
        modalEdit+='      type: "post",'
        modalEdit+='      url: "update/",'
        modalEdit+='      data: data,'
        modalEdit+=' beforeSend: function(xhr, settings) {'
        modalEdit+='if (!csrfSafeMethod(settings.type) && !this.crossDomain) {'
        modalEdit+='    xhr.setRequestHeader("X-CSRFToken", csrftoken);'
        modalEdit+='}'
        modalEdit+='      $("#modal-status-'+str(proyect.id)+'").html("<div class=\'alert alert-light\'>Realizando Cambios</div>");'
        modalEdit+='      },'
        modalEdit+='      success: function (response) {'
        modalEdit+='      $("#modal-status-'+str(proyect.id)+'")'
        modalEdit+='        .html(response);'
        modalEdit+='        location.reload();                 }'
        modalEdit+='    });'
        modalEdit+='  });'
        modalEdit+='  $("#btn-cancel-'+str(proyect.id)+'").click(()=>{'
        modalEdit+='    $("#input-project-'+str(proyect.id)+'").val("'+str(proyect.id)+'");'
        modalEdit+='    $("#btn-update-'+str(proyect.id)+'").attr("disabled","disabled");'
        modalEdit+='  });'
        modalEdit+='</script>'
    Alltable=altable+content+downtable+modalEdit+modalDelete
    return Alltable