// Task Management Application
// All data stored in memory (no localStorage)

let tasks = [];
let currentTaskId = null;
let taskToDelete = null;

// Initialize with sample data
function initializeSampleData() {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  const nextWeek = new Date(today);
  nextWeek.setDate(nextWeek.getDate() + 5);

  tasks = [
    {
      id: 1,
      title: "Complete Python Assignment",
      description: "Submit Student Management System project",
      category: "Study",
      priority: "High",
      deadline: tomorrow.toISOString().split('T')[0],
      completed: false,
      createdDate: today.toISOString().split('T')[0]
    },
    {
      id: 2,
      title: "TEDx Instagram Content Planning",
      description: "Plan next week's Instagram posts and engagement strategy",
      category: "College",
      priority: "Medium",
      deadline: new Date(today.getTime() + 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      completed: false,
      createdDate: today.toISOString().split('T')[0]
    },
    {
      id: 3,
      title: "Database Design Review",
      description: "Review database schema for the project",
      category: "Project",
      priority: "High",
      deadline: today.toISOString().split('T')[0],
      completed: false,
      createdDate: new Date(today.getTime() - 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    },
    {
      id: 4,
      title: "Purchase ANC Earbuds",
      description: "Compare OnePlus Nord Buds options",
      category: "Personal",
      priority: "Low",
      deadline: nextWeek.toISOString().split('T')[0],
      completed: false,
      createdDate: new Date(today.getTime() - 6 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    },
    {
      id: 5,
      title: "Attend Data Structures Class",
      description: "String matching algorithms and KMP implementation",
      category: "Study",
      priority: "High",
      deadline: tomorrow.toISOString().split('T')[0],
      completed: true,
      createdDate: new Date(today.getTime() - 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    }
  ];
}

// Generate unique ID
function generateId() {
  return tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1;
}

// Format date to readable string
function formatDate(dateString) {
  const date = new Date(dateString);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const taskDate = new Date(date);
  taskDate.setHours(0, 0, 0, 0);
  
  const diffTime = taskDate - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Tomorrow';
  if (diffDays === -1) return 'Yesterday';
  if (diffDays > 0 && diffDays <= 7) return `In ${diffDays} days`;
  if (diffDays < 0) return `${Math.abs(diffDays)} days ago`;
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// Check if task is urgent (within 24 hours)
function isUrgent(deadline) {
  const now = new Date();
  const deadlineDate = new Date(deadline);
  const diffHours = (deadlineDate - now) / (1000 * 60 * 60);
  return diffHours > 0 && diffHours <= 24;
}

// Update statistics
function updateStats() {
  const total = tasks.length;
  const completed = tasks.filter(t => t.completed).length;
  const pending = total - completed;
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;
  
  document.getElementById('totalTasks').textContent = total;
  document.getElementById('completedTasks').textContent = completed;
  document.getElementById('pendingTasks').textContent = pending;
  document.getElementById('completionRate').textContent = `${completionRate}%`;
  document.getElementById('progressPercentage').textContent = `${completionRate}%`;
  document.getElementById('progressFill').style.width = `${completionRate}%`;
}

// Render task card
function renderTaskCard(task, isUrgentTask = false) {
  const urgent = isUrgent(task.deadline) && !task.completed;
  
  return `
    <div class="task-card ${task.completed ? 'completed' : ''}" data-id="${task.id}">
      <div class="task-header">
        <div class="task-checkbox ${task.completed ? 'checked' : ''}" onclick="toggleTaskComplete(${task.id})">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <div class="task-main">
          <div class="task-title-row">
            <div class="task-title">${task.title}</div>
            <div class="priority-badge priority-${task.priority.toLowerCase()}">
              ${task.priority}
            </div>
          </div>
          ${task.description ? `<div class="task-description">${task.description}</div>` : ''}
          <div class="task-meta">
            <div class="task-meta-item">
              <span class="category-badge category-${task.category.toLowerCase()}">${task.category}</span>
            </div>
            <div class="deadline ${urgent ? 'urgent' : ''}">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              ${formatDate(task.deadline)}
            </div>
          </div>
        </div>
        <div class="task-actions">
          <button class="icon-btn" onclick="editTask(${task.id})" title="Edit task">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="icon-btn delete" onclick="confirmDelete(${task.id})" title="Delete task">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  `;
}

// Get filtered and sorted tasks
function getFilteredTasks() {
  const categoryFilter = document.getElementById('categoryFilter').value;
  const priorityFilter = document.getElementById('priorityFilter').value;
  const statusFilter = document.getElementById('statusFilter').value;
  const sortBy = document.getElementById('sortBy').value;
  
  let filtered = [...tasks];
  
  // Apply filters
  if (categoryFilter !== 'all') {
    filtered = filtered.filter(t => t.category === categoryFilter);
  }
  
  if (priorityFilter !== 'all') {
    filtered = filtered.filter(t => t.priority === priorityFilter);
  }
  
  if (statusFilter === 'completed') {
    filtered = filtered.filter(t => t.completed);
  } else if (statusFilter === 'pending') {
    filtered = filtered.filter(t => !t.completed);
  }
  
  // Apply sorting
  filtered.sort((a, b) => {
    if (sortBy === 'deadline') {
      return new Date(a.deadline) - new Date(b.deadline);
    } else if (sortBy === 'priority') {
      const priorityOrder = { 'High': 0, 'Medium': 1, 'Low': 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    } else if (sortBy === 'created') {
      return new Date(b.createdDate) - new Date(a.createdDate);
    }
    return 0;
  });
  
  return filtered;
}

// Render all tasks
function renderTasks() {
  const filtered = getFilteredTasks();
  const tasksList = document.getElementById('tasksList');
  const emptyState = document.getElementById('emptyState');
  const taskCount = document.getElementById('taskCount');
  
  if (filtered.length === 0) {
    tasksList.innerHTML = '';
    emptyState.style.display = 'block';
    taskCount.textContent = '0 tasks';
  } else {
    tasksList.innerHTML = filtered.map(task => renderTaskCard(task)).join('');
    emptyState.style.display = 'none';
    taskCount.textContent = `${filtered.length} ${filtered.length === 1 ? 'task' : 'tasks'}`;
  }
  
  // Render urgent tasks
  renderUrgentTasks();
}

// Render urgent tasks section
function renderUrgentTasks() {
  const urgentTasks = tasks.filter(t => isUrgent(t.deadline) && !t.completed);
  const urgentSection = document.getElementById('urgentSection');
  const urgentTasksList = document.getElementById('urgentTasksList');
  
  if (urgentTasks.length > 0) {
    urgentSection.style.display = 'block';
    urgentTasksList.innerHTML = urgentTasks.map(task => renderTaskCard(task, true)).join('');
  } else {
    urgentSection.style.display = 'none';
  }
}

// Toggle task completion
function toggleTaskComplete(id) {
  const task = tasks.find(t => t.id === id);
  if (task) {
    task.completed = !task.completed;
    updateStats();
    renderTasks();
  }
}

// Open modal for adding new task
function openAddTaskModal() {
  currentTaskId = null;
  document.getElementById('modalTitle').textContent = 'Add New Task';
  document.getElementById('taskForm').reset();
  
  // Set minimum date to today
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('taskDeadline').min = today;
  
  document.getElementById('taskModal').classList.add('active');
}

// Edit task
function editTask(id) {
  const task = tasks.find(t => t.id === id);
  if (!task) return;
  
  currentTaskId = id;
  document.getElementById('modalTitle').textContent = 'Edit Task';
  document.getElementById('taskTitle').value = task.title;
  document.getElementById('taskDescription').value = task.description;
  document.getElementById('taskCategory').value = task.category;
  document.getElementById('taskPriority').value = task.priority;
  document.getElementById('taskDeadline').value = task.deadline;
  
  document.getElementById('taskModal').classList.add('active');
}

// Close task modal
function closeTaskModal() {
  document.getElementById('taskModal').classList.remove('active');
  currentTaskId = null;
}

// Save task (add or update)
function saveTask(event) {
  event.preventDefault();
  
  const title = document.getElementById('taskTitle').value.trim();
  const description = document.getElementById('taskDescription').value.trim();
  const category = document.getElementById('taskCategory').value;
  const priority = document.getElementById('taskPriority').value;
  const deadline = document.getElementById('taskDeadline').value;
  
  if (!title || !category || !priority || !deadline) {
    alert('Please fill in all required fields');
    return;
  }
  
  if (currentTaskId) {
    // Update existing task
    const task = tasks.find(t => t.id === currentTaskId);
    if (task) {
      task.title = title;
      task.description = description;
      task.category = category;
      task.priority = priority;
      task.deadline = deadline;
    }
  } else {
    // Add new task
    const newTask = {
      id: generateId(),
      title,
      description,
      category,
      priority,
      deadline,
      completed: false,
      createdDate: new Date().toISOString().split('T')[0]
    };
    tasks.push(newTask);
  }
  
  closeTaskModal();
  updateStats();
  renderTasks();
}

// Confirm delete
function confirmDelete(id) {
  taskToDelete = id;
  document.getElementById('deleteModal').classList.add('active');
}

// Close delete modal
function closeDeleteModal() {
  document.getElementById('deleteModal').classList.remove('active');
  taskToDelete = null;
}

// Delete task
function deleteTask() {
  if (taskToDelete) {
    tasks = tasks.filter(t => t.id !== taskToDelete);
    closeDeleteModal();
    updateStats();
    renderTasks();
  }
}

// Reset filters
function resetFilters() {
  document.getElementById('categoryFilter').value = 'all';
  document.getElementById('priorityFilter').value = 'all';
  document.getElementById('statusFilter').value = 'all';
  document.getElementById('sortBy').value = 'deadline';
  renderTasks();
}

// Initialize app
function init() {
  initializeSampleData();
  updateStats();
  renderTasks();
  
  // Event listeners
  document.getElementById('addTaskBtn').addEventListener('click', openAddTaskModal);
  document.getElementById('closeModal').addEventListener('click', closeTaskModal);
  document.getElementById('cancelBtn').addEventListener('click', closeTaskModal);
  document.getElementById('taskForm').addEventListener('submit', saveTask);
  
  document.getElementById('closeDeleteModal').addEventListener('click', closeDeleteModal);
  document.getElementById('cancelDeleteBtn').addEventListener('click', closeDeleteModal);
  document.getElementById('confirmDeleteBtn').addEventListener('click', deleteTask);
  
  document.getElementById('categoryFilter').addEventListener('change', renderTasks);
  document.getElementById('priorityFilter').addEventListener('change', renderTasks);
  document.getElementById('statusFilter').addEventListener('change', renderTasks);
  document.getElementById('sortBy').addEventListener('change', renderTasks);
  document.getElementById('resetFiltersBtn').addEventListener('click', resetFilters);
  
  // Close modals on background click
  document.getElementById('taskModal').addEventListener('click', function(e) {
    if (e.target === this) closeTaskModal();
  });
  
  document.getElementById('deleteModal').addEventListener('click', function(e) {
    if (e.target === this) closeDeleteModal();
  });
}

// Start the app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}