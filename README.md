# Smart Attendance System backend API

### Deployed on vercel at <https://sas-backend-app.vercel.app/>
### Frontend deployed on firebase at <https://smart-attendance-13c82.firebaseapp.com/>

This attendance system allows professors to view student attendance in their subject and allows students to view their own attendance

Routes and their description:
  /login Method: POST PROTECTED Description: send username and password for login and get the user token
    usernames and role are assigned by the system admins
    
  /logout Method: POST PROTECTED Description: logout of the system and delete the user token

  /getSubjectAttendance/<int:subject>/ Method: GET PROTECTED Description: if the user requesting this route is a student then they will get their own attendance on this specific subject
    if the requesting user is a professor and they teach this subject then they will get the attendance in this subject
  
  /markAttendance/ Method: POST PROTECTED Description: send student ID and subject ID to mark that the student attended this subject

  /getProfile Method: GET PROTECTED Description: get the current user profile

  /getSubject Method: GET PROTECTED Description: get the current user subjects

  /getLevels/  Method: GET PROTECTED Description: if the user is a professor get the level of subjects they teach

  /getLevelSubjects/<int:level>/ Method: GET PROTECTED Description: get all the subjects in a single level

  /getLevelStudents/<int:level>/ Method: GET PROTECTED Description: get all the students in a singel level
