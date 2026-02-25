const Workspace = {
  projects: [
    {name: 'Project 1', status: 'planning', priority: 1},
    {name: 'Project 2', status: 'research', priority: 2},
    {name: 'Project 3', status: 'todo', priority: 3}
  ],
  tasks: [
    {id: 1, description: 'Complete documentation', priority: 1},
    {id: 2, description: 'Write unit tests', priority: 1},
    {id: 3, description: 'Optimize database queries', priority: 2}
  ],

  updateStatus(projectName, newStatus) {
    this.projects = this.projects.map(p =>
      p.name === projectName ? {...p, status: newStatus} : p
    );
    return this;
  },

  addTask(task) {
    this.tasks.push(task);
    return this;
  }
};

// Export the workspace instance
module.exports = Workspace;