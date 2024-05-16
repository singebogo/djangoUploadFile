import os, uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def upload_files(request):
    if request.method == "GET":
        return render(request, 'ajaxfiles_upload.html', )
    if request.method == 'POST':
        files = request.FILES.getlist('files[]', None)
        #print(files)
        for f in files:
            handle_uploaded_file(f)
        return JsonResponse({'msg':'<span style="color: green;">File successfully uploaded</span>'})
    else:
        return render(request, 'ajaxfiles_upload.html', )

def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path

# def handle_uploaded_file(f):
#     with open(f.name, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)