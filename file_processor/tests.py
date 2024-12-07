import io
from django.test import TestCase
from django.urls import reverse
from file_processor.models import FileTask 
import uuid

class AllTasksViewTest(TestCase):
    def setUp(self):
        # Create sample FileTask objects
        FileTask.objects.create(
            task_id=uuid.uuid4(),
            file_name='file1.txt',
            status='completed',
            result='50'
        )
        FileTask.objects.create(
            task_id=uuid.uuid4(),
            file_name='file2.txt',
            status='processing',
            result=None
        )

    def test_all_tasks_returns_correct_data(self):
        # send request
        url = reverse('all_tasks')
        response = self.client.get(url)

        # Assert 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert
        expected_data = [
            {
                'task_id': str(FileTask.objects.all()[0].task_id),
                'file_name': 'file1.txt',
                'status': 'completed',
                'result': '50'
            },
            {
                'task_id': str(FileTask.objects.all()[1].task_id),
                'file_name': 'file2.txt',
                'status': 'processing',
                'result': None
            },
        ]
        self.assertJSONEqual(response.content, expected_data)

    def test_all_tasks_returns_empty_list_if_no_tasks(self):
        # Delete all tasks
        FileTask.objects.all().delete()

        # Send request
        url = reverse('all_tasks')
        response = self.client.get(url)

        # Assert
        self.assertJSONEqual(response.content, [])


class DeleteAllTasksviewTest(TestCase):
    def setUp(self):
        # Create sample FileTask objects
        FileTask.objects.create(
            task_id=uuid.uuid4(),
            file_name='file1.txt',
            status='completed',
            result='50'
        )
        FileTask.objects.create(
            task_id=uuid.uuid4(),
            file_name='file2.txt',
            status='processing',
            result=None
        )
        
    def test_delete_all_tasks_success(self):
        # Send request
        url = reverse('delete_all_tasks')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(FileTask.objects.count(), 0)
        
        # expected_response = {"message": "All tasks have been successfully deleted."}
        
        self.assertJSONEqual(response.content,{"message":"All tasks have been successfully deleted."})
        
        
class FileStatusViewTest(TestCase):
    def setUp(self):
        self.task = FileTask.objects.create(
            task_id=uuid.uuid4(),
            file_name='file1.txt',
            status='completed',
            result='50'
        )
        self.url = reverse('file_status')
    
    def test_file_status_seccess(self):
        url = f"{self.url}?task_id={self.task.task_id}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        expected_data = {
            'task_id': str(self.task.task_id),
            'file_name': 'file1.txt',
            'status': 'completed',
            'result': '50',
        }
        
        self.assertJSONEqual(response.content, expected_data)
        
    def test_file_status_notFound(self):
        url = f"{self.url}?task_id={uuid.uuid4()}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
        
        self.assertJSONEqual(response.content, {'error': 'Task not found'})
        
    def test_file_status_taskId_notFound(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 400)
        
        self.assertJSONEqual(response.content, {'error': 'Task id is required'})
        
    
# class FileUploadViewTest(TestCase):
#     def setUp(self):
#         self.url = reverse('upload_file') 
    
#     def test_file_upload_success(self):
#         file_content = "Sample file content"
#         file = io.BytesIO(file_content.encode('utf-8'))  
#         file.name = 'test_file.txt' 
        
#         response = self.client.post(self.url, {'file': file})

#         self.assertEqual(response.status_code, 201)
        
#         task = FileTask.objects.get(file_name='test_file.txt')
#         self.assertIsNotNone(task)
#         self.assertEqual(task.file_content, file_content)
#         self.assertEqual(task.status, 'processing')
        
#         self.assertIn('task_id', response.json())
#         self.assertEqual(response.json()['task_id'], str(task.task_id))
