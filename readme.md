
# Project Title

Student Conduct Tracker


# Student CLI Application

This CLI application allows users to manage student records. It provides commands for creating students, searching for them, reviewing their performance, and viewing reviews.

## Commands

### 1. Create a Student

```bash
flask student create

```
Description: Creates a new student record.
The user will be prompted for a first and last name for the student.  Then the student will be created and stored in the database

Output: Displays a success message with the student's ID.

```bash
flask student search
```

Description: Searches for a student using their id. After entering the command the user will be prompted for the student's ID.

Output: Displays the student's information if successful or the string "Student does not exist." when unsuccessful.

```bash
flask student review
```

Description: Reviews a student. The user will be prompted to enter a student's ID. Then will be asked to enter the content of the review.

Output: Displays the review in JSON format if successful or prints the string "Review failed because a student is not associated with that ID." if unsuccessful

```bash
flask student view_reviews
```

Description: Returns all reviews for a student. The user will prompted for the student's ID.

Output: Displays all reviews for that student in JSON format if successful otherwise prints the string "Student does not exist.".


