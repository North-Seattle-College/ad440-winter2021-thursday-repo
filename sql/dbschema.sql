CREATE TABLE users (
  userId INT PRIMARY KEY IDENTITY(1,1),
  firstName VARCHAR(50) NOT NULL,
  lastName VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  deleted INT DEFAULT 0 NOT NULL
);

CREATE TABLE tasks(
  taskId INT PRIMARY KEY IDENTITY(1,1),
  title VARCHAR(50),
  description VARCHAR(400),
  createdTime DATETIME NOT NULL,
  deleted INT NOT NULL DEFAULT 0
);

CREATE TABLE userTasks(
  taskId INT NOT NULL,
  userId INT NOT NULL,
  assignedDate DATETIME NOT NULL,
  completed INT NOT NULL DEFAULT 0,
  
  CONSTRAINT FK_Task_User FOREIGN KEY (taskId)
    REFERENCES  tasks(taskId)
    ON DELETE CASCADE,
  CONSTRAINT FK_User_Task FOREIGN KEY (userId)
    REFERENCES  users(userId)
    ON DELETE CASCADE
);

-- useful statements =>
-- rename a column: EXEC sp_RENAME 'tableName.columnOldName' , 'columnNewName', 'COLUMN'
-- add a column: ALTER TABLE tableName ADD columnName columnType null/not null;