CREATE TABLE users (
  userId INT PRIMARY KEY UNIQUE AUTO_INCREMENT,
  firstName VARCHAR(50) NOT NULL,
  lastName VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  deleted INT DEFAULT 0 NOT NULL
);

CREATE TABLE tasks(
  taskId INT PRIMARY KEY UNIQUE AUTO_INCREMENT,
  task VARCHAR(300),
  createdTime DATETIME NOT NULL,
  deleted INT NOT NULL DEFAULT 0
);

CREATE TABLE userTasks(
  taskId INT NOT NULL,
  userId INT NOT NULL,
  assignedDate DATETIME NOT NULL,
  accomplished INT NOT NULL DEFAULT 0,
  
  CONSTRAINT FK_Task_User FOREIGN KEY (taskId)
    REFERENCES  tasks(taskId)
    ON DELETE CASCADE,
  CONSTRAINT FK_User_Task FOREIGN KEY (userId)
    REFERENCES  users(userId)
    ON DELETE CASCADE
);

INSERT INTO  users (userId, firstName, lastName, email, deleted) 
VALUES 
(1,"Jorden","Salazar","luctus.Curabitur.egestas@dictum.ca",0),
(2,"Aidan","Weber","fermentum.convallis.ligula@purus.com",0),
(3,"Macaulay","Rosa","porta@aliquameuaccumsan.ca",1),
(4,"Jerome","Perez","Nulla@nullaatsem.edu",1),
(5,"Leroy","Knowles","sem.Pellentesque.ut@aliquetlobortis.com",0),
(6,"Naomi","Garcia","nisi.sem@mollisvitae.com",0),
(7,"Anjolie","Gibson","urna@adipiscingligula.edu",1),
(8,"Carly","Haley","fringilla.purus@ametante.edu",0),
(9,"Reuben","Lyons","quam.a@ornareegestas.com",0),
(10,"Marshall","Shaffer","In@purusNullam.ca",0),
(11,"Alexa","Finch","Quisque.ornare@anequeNullam.net",0),
(12,"Hoyt","Mcintosh","semper.et.lacinia@liberomauris.ca",0),
(13,"Yetta","Ochoa","lorem.vitae.odio@non.com",1),
(14,"Joel","Benson","quis.turpis.vitae@eu.net",0),
(15,"Channing","Dickerson","semper.egestas.urna@sitamet.edu",0),
(16,"Rhoda","Ayala","elementum@dui.ca",1),
(17,"Sean","Reilly","Curae.Phasellus@egestasurna.edu",1),
(18,"Chase","Lowery","lacus.varius@mienimcondimentum.edu",1),
(19,"Daniel","Gardner","metus.urna@antebibendum.net",1),
(20,"Ivy","Kane","erat@elit.org",1);


INSERT INTO tasks (taskId, task, createdTime, deleted)
VALUES 
(1,"Design the solution","2021-09-26 04:04:00",0),
(2,"Prepare for implementation","2020-08-13 08:40:31",1),
(3,"Prepare the test/QA environment	","2021-05-07 05:46:38",1),
(4,"Install the product in the test/QA environment.	","2021-11-15 02:43:15",1),
(5,"Implement distributed data feeds (this can be done in parallel with the Source/390 data feed implementation)","2020-06-16 00:50:45",0),
(6,"Implement Source/390 data feeds on the test LPAR (this can be done in parallel with the distributed data feed implementation)	","2020-04-24 09:18:32",0),
(7,"Implement a business system in the test/QA environment","2020-09-13 06:15:23",0),
(8,"Schedule jobs","2021-02-13 17:08:45",0),
(9,"Prepare the production environment","2020-05-06 12:49:16",0),
(10,"Install the product in the production environment","2020-08-19 03:13:47",1),
(11,"Implement distributed data feeds in the production environment","2021-09-09 22:59:40",0),
(12,"Implement Source/390 data feeds in the production environment","2020-01-29 16:58:17",1),
(13,"Implement a business system in the production environment","2020-01-20 03:39:31",0),
(14,"Install the history server","2020-06-11 16:04:29",1),
(15,"Install the Health Monitor","2020-01-13 02:29:15",0);


INSERT INTO userTasks (taskId, userId, assignedDate, accomplished)
VALUES
(8,6,"2021-01-09 20:50:40",1),
(11,10,"2021-01-04 08:06:44",0),
(9,20,"2021-01-15 21:13:36",1),
(10,14,"2021-01-22 06:51:27",0),
(10,15,"2021-01-29 07:28:57",0),
(7,7,"2021-01-12 18:19:04",1),
(1,17,"2021-01-07 20:25:45",1),
(11,10,"2021-01-19 03:25:09",1),
(5,17,"2021-01-24 02:05:16",0),
(5,5,"2021-01-22 03:05:04",1),
(5,20,"2021-01-09 14:59:31",1),
(11,10,"2021-01-25 16:13:06",1),
(7,20,"2021-01-15 13:34:30",0),
(4,9,"2021-01-01 18:04:32",0),
(15,19,"2021-01-03 11:09:47",0),
(11,10,"2021-01-19 11:49:59",1),
(7,19,"2021-01-15 06:22:02",1),
(15,17,"2021-01-02 12:10:51",1),
(1,19,"2021-01-03 22:29:43",1),
(1,16,"2021-01-26 05:19:07",1),
(15,20,"2021-01-19 17:49:41",0),
(9,9,"2021-01-20 03:11:34",1),
(5,11,"2021-01-12 08:28:42",0),
(4,17,"2021-01-02 14:29:47",0),
(8,14,"2021-01-17 09:12:46",0);