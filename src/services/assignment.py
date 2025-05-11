from datetime import datetime
from typing import List, Optional

from repositories.answer import AnswerRepository
from repositories.assignment import AssignmentRepository
from repositories.course import CourseRepository
from repositories.user import UserRepository
from schemas.assignment import AssignmentModel, Assignment, AssignmentCourse
from utils.hash import get_hash_string
from utils.jwt import decode_data

STUDENT = 'student'
TEACHER = 'teacher'
PENDING = 'pending'
IN_REVIEW = 'in_review'
GRADED = 'graded'

class AssignmentService():
    def __init__(self):
        self.answer_repository = AnswerRepository()
        self.assignment_repository = AssignmentRepository()
        self.user_repository = UserRepository()
        self.course_repository = CourseRepository()

    def create_assignment(self, assignment: AssignmentModel, course_id: str, token: str):
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        return self.assignment_repository.create_assignment(assignment, course_id)

    def update_assignment(self, assignment: AssignmentModel, assignment_id: str, token: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        self.assignment_repository.update_assignment(assignment, assignment_id)
        return True

    def delete_assignment(self, assignment_id: str, token: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        self.assignment_repository.delete_assignment(assignment_id)
        return True

    def get_assignments(self, course_id: str, token: str) -> Optional[List[Assignment]]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] not in [STUDENT, TEACHER] or not data[0][5]:
            return None
        data = self.assignment_repository.get_assignments(course_id)
        response: List[Assignment] = []
        for i in data:
            response.append(Assignment(id=str(i[0]), name=i[1], started_at=i[2], ended_at=i[3]))
        return response

    def get_homeworks(self, token: str) -> Optional[List[AssignmentCourse]]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != STUDENT or not data[0][5]:
            return None
        student_courses = self.course_repository.get_courses(data[0][6])
        if not student_courses:
            return []
        response: List[AssignmentCourse] = []
        for student_course in student_courses:
            suitable_assignments: List[Assignment] = []
            course_assignments = self.assignment_repository.get_assignments(student_course[0])
            for course_assignment in course_assignments:
                if datetime.now() >= course_assignment[2] and (not course_assignment[3] or datetime.now() < course_assignment[3]):
                    assignment_answers = self.answer_repository.get_answers(data[0][6], course_assignment[0])
                    if not assignment_answers:
                       suitable_assignments.append(Assignment(id=str(course_assignment[0]), name=course_assignment[1], 
                                                              started_at=course_assignment[2], ended_at=course_assignment[3],
                                                              status=PENDING))
                    else:
                        has_assessment = False
                        for assignment_answer in assignment_answers:
                           if assignment_answer[5]:
                               has_assessment = True
                               suitable_assignments.append(Assignment(id=str(course_assignment[0]), name=course_assignment[1], 
                                                              started_at=course_assignment[2], ended_at=course_assignment[3],
                                                              status=GRADED))
                        if not has_assessment:
                            suitable_assignments.append(Assignment(id=str(course_assignment[0]), name=course_assignment[1], 
                                                            started_at=course_assignment[2], ended_at=course_assignment[3],
                                                            status=IN_REVIEW))
                else:
                    continue
            if suitable_assignments:
                response.append(AssignmentCourse(course_id=str(student_course[0]), course_name=student_course[1], assignments=suitable_assignments))
        return response