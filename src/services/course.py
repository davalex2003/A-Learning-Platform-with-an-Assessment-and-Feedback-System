from os import remove
from typing import Optional, List

from repositories.course import CourseRepository
from repositories.user import UserRepository
from schemas.common import Course
from schemas.course import CourseModel, CourseAdditionsResponse200, User, FullName
from utils.hash import get_hash_string
from utils.jwt import decode_data

ADMIN = 'admin'
TEACHER = 'teacher'
STUDENT = 'student'
LINK = 'link'
MATERIAL = 'material'

class CourseService():
    def __init__(self):
        self.course_repository = CourseRepository()
        self.user_repository = UserRepository()

    def create_course(self, course: CourseModel, token: str) -> Optional[str]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        return self.course_repository.create_course(course, data[0][6])
    
    def update_course(self, course: CourseModel, token: str, course_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] not in [TEACHER, ADMIN] or not data[0][5]:
            return False
        self.course_repository.update_course(course, course_id)
        return True
    
    def delete_course(self, token: str, course_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] not in [TEACHER, ADMIN] or not data[0][5]:
            return False
        self.course_repository.delete_course(course_id)
        return True

    def get_courses_list(self, token: str, search_query: Optional[str] = None) -> Optional[List[Course]]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        user_id = data[0][6]
        data = self.course_repository.get_courses_list(user_id)
        response: List[Course] = []
        for i in data:
            if search_query:
                if search_query in i[1] or search_query in i[2]:
                    response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[5]))
            else:
                response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[5]))   
        return response
    
    def insert_course_link(self, token: str, course_id: str, link: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        links = self.course_repository.get_course_links(course_id)
        if links is None:
            return True
        links = links[0]
        if links is None:
            links = [link]
        else:
            links.append(link)
        self.course_repository.update_course_links(course_id, links)
        return True

    async def insert_course_material(self, token: str, course_id: str, material) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        materials = self.course_repository.get_course_materials(course_id)
        if materials is None or not materials[0]:
            materials = [material.filename]
        else:
            materials[0].append(material.filename)
        self.course_repository.update_course_materials(course_id, materials)
        with open(material.filename, "wb") as f:
            content = await material.read()
            f.write(content)
        return True
    
    def get_links_and_materials(self, token: str, course_id: str) -> Optional[CourseAdditionsResponse200]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if not data[0][5]:
            return None
        additions = self.course_repository.get_links_and_materials(course_id)
        links = []
        materials = []
        if additions is None:
            return CourseAdditionsResponse200(materials=materials, links=links)
        if additions[0] is not None:
            for i in range(len(additions[0])):
                links.append({'id': str(i + 1), 'name': additions[0][i]})
        if additions[1] is not None:
            for i in range(len(additions[1])):
                materials.append({'id': str(i + 1), 'name': additions[1][i]})
        return CourseAdditionsResponse200(materials=materials, links=links)
    
    def get_course_material(self, token: str, course_id: str, addition_id: str):
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if not data[0][5]:
            return None
        materials = self.course_repository.get_course_materials(course_id)
        if materials is None or materials[0] is None:
            return None
        materials = materials[0]
        if len(materials) < int(addition_id):
            return None
        return materials[int(addition_id) - 1]
    
    def delete_course_addition(self, token: str, course_id: str, addition_id: str, addition_type: str):
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        additions = self.course_repository.get_links_and_materials(course_id)
        if additions is None:
            return True
        if addition_type == LINK:
            links = additions[0]
            if links is None:
                return True
            links.pop(int(addition_id) - 1)
            self.course_repository.update_course_links(course_id, links)
        else:
            materials = additions[1]
            if materials is None:
                return True
            material = materials[int(addition_id) - 1]
            materials.pop(int(addition_id) - 1)
            remove(material)
            self.course_repository.update_course_materials(course_id, materials)
        return True

    def add_user_course_link(self, token: str, course_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != STUDENT or not data[0][5]:
            return False
        self.course_repository.add_course_user_link(data[0][6], course_id)
        return True

    def delete_user_course_link(self, token: str, course_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != STUDENT or not data[0][5]:
            return False
        self.course_repository.delete_course_user_link(data[0][6], course_id)
        return True
    
    def get_courses_student_list(self, token: str, search_query: Optional[str] = None) -> Optional[List[Course]]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != STUDENT or not data[0][5]:
            return None
        user_id = data[0][6]
        data = self.course_repository.get_courses(user_id)
        response: List[Course] = []
        for i in data:
            if search_query:
                if search_query in i[1] or search_query in i[2]:
                    response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[3]))
            else:
                response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[3]))   
        return response

    def get_course_users_list(self, token: str, course_id: str) -> Optional[List[User]]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        data = self.course_repository.get_course_users_list(course_id)
        response: List[User] = []
        for i in data:
            response.append(User(id=str(i[0]), full_name=FullName(first_name=i[1], second_name=i[2], middle_name=i[3]), email=i[4]))
        return response