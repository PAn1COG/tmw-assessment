import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from file_processor.models import FileTask
import subprocess
from threading import Thread

def renderAll_tasks(request):
    return render(request, 'allTasks.html')

def index(request):
    return render(request, 'index.html')

def status(request):
    return render(request, 'status.html')

def async_process_file(task_id, file_content):
    # process the file using the process_file.py script as soon as file
    try:
        # Run the subprocess
        result = subprocess.run(
            ["python", "process_file.py", json.dumps({"file_content": file_content})],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = json.loads(result.stdout)

        # Update the database
        task = FileTask.objects.get(task_id=task_id)
        task.status = output.get("status", "error")
        task.result = output.get("result")
        task.save()
        
    except Exception as e:
        print(e)
        task = FileTask.objects.get(task_id=task_id)
        print(task.file_content)
        task.status = "error"
        task.result = None
        task.save()


# to upload a file
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            file_content = file.read().decode('utf-8') 
            task = FileTask.objects.create(
                file_name=file.name,
                file_content=file_content,
                status='processing'
            )
            
            Thread(target=async_process_file, args=(task.task_id, file_content)).start()

            return JsonResponse({'task_id': str(task.task_id)}, status=201)
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# to get file status and results
def file_status(request):
    task_id = request.GET.get('task_id')
    try:
        task = FileTask.objects.get(task_id=task_id)
        response = {
            'task_id': str(task.task_id),
            'file_name': task.file_name,
            'status': task.status,
            'result': task.result
        }
        return JsonResponse(response)
    except FileTask.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

# Endpoint to get all tasks
def all_tasks(request):
    tasks = FileTask.objects.all().values('task_id', 'file_name', 'status', 'result')
    return JsonResponse(list(tasks), safe=False)

def delete_all_tasks(request):
    try:
        # Delete all records in the FileTask model  
        FileTask.objects.all().delete()
        return JsonResponse({'message': 'All tasks have been successfully deleted.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)