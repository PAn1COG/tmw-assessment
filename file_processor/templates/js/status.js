document.addEventListener("DOMContentLoaded", () => {
  const taskId = new URL(window.location.href).searchParams.get("task_id");
  const taskStatusElement = document.getElementById("task-status");
  const taskResultElement = document.getElementById("task-result");
  const loaderContainer = document.getElementById("loader-container");

  // Function to fetch status
  const fetchTaskStatus = () => {
    fetch(`http://127.0.0.1:8000/status/?task_id=${taskId}`)
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("task-id").textContent = data.task_id;
        document.getElementById("file-name").textContent = data.file_name;
        taskStatusElement.textContent = data.status;

        if (data.error) {
          alert("Task not found. Please check the file or try again.");
          window.location.href = 'index.html';
        }

        if (data.status === "processing") {
          // Only fetch if still processing
          loaderContainer.classList.remove("hidden");
        } else {
          loaderContainer.classList.add("hidden");
          taskResultElement.textContent = `Result: ${data.result}`;
          taskResultElement.classList.remove("hidden");
          // Stop when processing is complete
          clearInterval(statusInterval);
        }
      })
      .catch((error) => {
        console.error("Error fetching task status:", error);
        taskStatusElement.textContent = "Error occurred";
        loaderContainer.classList.add("hidden");
        // Stop if there is error
        clearInterval(statusInterval);
      });
  };

  // Initial fetch
  fetchTaskStatus();
  const statusInterval = setInterval(fetchTaskStatus, 3000);
});
