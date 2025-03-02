document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('task-list');

    // 加载任务
    const loadTasks = async () => {
        const response = await fetch('/tasks');
        const tasks = await response.json();
        taskList.innerHTML = '';
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.textContent = task[1];
            if (task[2] === 1) {
                li.classList.add('completed');
            }

            const taskActions = document.createElement('div');
            taskActions.className = 'task-actions';

            const completeBtn = document.createElement('button');
            completeBtn.textContent = '✅ 完成';
            completeBtn.className = 'complete-btn';
            completeBtn.addEventListener('click', () => completeTask(task[0]));

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = '❌ 删除';
            deleteBtn.className = 'delete-btn';
            deleteBtn.addEventListener('click', () => deleteTask(task[0]));

            taskActions.appendChild(completeBtn);
            taskActions.appendChild(deleteBtn);
            li.appendChild(taskActions);
            taskList.appendChild(li);
        });
    };

    // 添加任务
    addTaskBtn.addEventListener('click', async () => {
        const task = taskInput.value.trim();
        if (task) {
            await fetch('/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task })
            });
            taskInput.value = '';
            loadTasks();
        }
    });

    // 标记任务完成
    const completeTask = async (taskId) => {
        await fetch(`/tasks/${taskId}/complete`, { method: 'PUT' });
        loadTasks();
    };

    // 删除任务
    const deleteTask = async (taskId) => {
        await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
        loadTasks();
    };

    // 初始化加载任务
    loadTasks();
});