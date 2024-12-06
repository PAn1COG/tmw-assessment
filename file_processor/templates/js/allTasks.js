document.addEventListener('DOMContentLoaded', () => {
    const tasksContainer = document.getElementById('tasks-container');

    // Function to fetch all tasks and display them
    const fetchAllTasks = () => {
        fetch('http://127.0.0.1:8000/all_tasks/')
            .then(response => response.json())
            .then(tasks => {
                tasksContainer.innerHTML = ''; 

                if (tasks.length > 0) {
                    tasks.forEach(task => {
                        const taskElement = document.createElement('div');
                        taskElement.classList.add('border', 'p-4', 'rounded', 'mb-4');
                        taskElement.id = `task-${task.task_id}`;
                        taskElement.innerHTML = `
                            <p><strong>Task ID:</strong> ${task.task_id}</p>
                            <p><strong>File Name:</strong> ${task.file_name}</p>
                            <p><strong>Status:</strong> <span id="status-${task.task_id}">${task.status}</span></p>
                            <p><strong>Result:</strong> <span id="result-${task.task_id}">${task.result || 'N/A'}</span></p>
                        `;
                        tasksContainer.appendChild(taskElement);

                        //display loading indicator for tasks that are processing
                        if (task.status === 'processing') {
                            const loader = document.createElement('div');
                            loader.classList.add('loader', 'my-2');
                            if (task.status === 'processing') {
                                const loader = document.createElement('div');
                                loader.classList.add('loader');
                                taskElement.appendChild(loader);
                            }
                            // loader.innerHTML = '<p>Processing...</p>';
                        }
                    });
                } else {
                    tasksContainer.innerHTML = '<p class="text-center text-gray-500">No tasks found.</p>';
                }
            })
            .catch(error => console.error('Error fetching tasks:', error));
    };

    // Initial fetch
    fetchAllTasks();
    // Poll for updates every 15 seconds to refresh the task list if needed
    setInterval(fetchAllTasks, 15000);
});
