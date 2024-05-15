from django.shortcuts import render, redirect
from .models import File
from .forms import FileUploadForm, FileUploadModelForm
import os
import uuid
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat

# Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")
    return render(request, 'file_list.html', {'files': files})

# Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")
            new_file = File()
            new_file.file = handle_uploaded_file(raw_file)
            new_file.upload_method = upload_method
            new_file.save()
            return redirect("file_upload:file_list")
    else:
        form = FileUploadForm()

    return render(request, 'upload_form.html',
                  {'form': form, 'heading': 'Upload files with Regular Form'}
                 )

"""
handle_uploaded_file方法里文件写入地址必需是包含/media/的绝对路径，如果/media/files/xxxx.jpg
，而该方法返回的地址是相对于/media/文件夹的地址，如/files/xxx.jpg。存在数据中字段的是相对地址，而不是绝对地址。
"""
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



def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # 一句话足以
            return redirect("file_upload:file_list")
    else:
        form = FileUploadModelForm()

    return render(request, 'upload_form.html',
                  {'form': form,'heading': 'Upload files with ModelForm'}
                 )

# handling AJAX requests
def ajax_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Obtain the latest file list
            files = File.objects.all().order_by('-id')
            data = []
            for file in files:
                data.append({
                    "url": file.file.url,
                    "size": filesizeformat(file.file.size),
                    })
            return JsonResponse(data, safe=False)
    else:
        form = FileUploadModelForm()
    return render(request, 'ajax_upload.html',
                  {'form': form, 'heading': 'Upload files with Regular Form'}
            )