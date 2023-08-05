from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from psu_base.classes.Log import Log
from psu_base.services import auth_service
from psu_base.decorators import require_authority, require_authentication
from psu_upload.services import upload_service, retrieval_service


log = Log()

# ToDo: Error Handling/Messages


@require_authentication()
def index(request):
    """
    Menu of ...
    """
    log.trace()

    uploaded_files = retrieval_service.get_all_files()

    return render(
        request, 'upload_sample.html',
        {'uploaded_files': uploaded_files}
    )


@require_authentication()
def upload_file(request):
    """
    Upload a file and store it in S3
    """
    log.trace()

    if request.method == 'POST':
        if request.POST.get('display_only'):
            files = upload_service.read_uploaded_files(request, 'uploaded_file', convert_to_string="base64")
            return render(
                request, 'read_sample.html',
                {'files': files}
            )
        else:
            ufs = upload_service.upload_files(request, 'uploaded_file', 'test-', 'Tests')

    return redirect('upload:sample')


@require_authentication()
def file_attachment(request, file_id):
    """
    Retrieve a specified file and display as attachment.

    Note: this is to be used as a sample, as each app will probably have to verify
    permissions based on its own specific roles and business logic
    """
    log.trace()

    if upload_service.using_s3():
        # This is only for database files
        return HttpResponseForbidden()

    # Retrieve the file
    file = retrieval_service.get_file_query().get(pk=file_id)

    if not file:
        return Http404()

    if not auth_service.is_logged_in():
        return HttpResponseForbidden()

    if auth_service.get_user().username != file.owner and not auth_service.has_authority('DynamicPowerUser'):
        return HttpResponseForbidden()

    # Otherwise, is owner or admin
    filename = file.filename
    response = HttpResponse(content_type=file.content_type)

    if request.GET.get('download'):
        # Force browser to download file
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

    response.write(file.file)
    return response
