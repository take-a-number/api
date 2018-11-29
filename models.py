from collections import namedtuple
from enum import Enum


Course = namedtuple('Course', ['abbreviation', 'description', 'id', 'teaching_assistant_join_code'])
# interface ICourse {
#   abbreviation: string;
#   description: string;
#   id: string;
#   teachingAssistantJoinCode?: string,
# }


OfficeHours = namedtuple('OfficeHours',
                         'course_abbreviation, student_join_code, teaching_assistants, students, student_sessions, teaching_assistant_sessions')
# interface IOfficeHours {
#   courseAbbreviation: string;
#   studentJoinCode?: string;
#   teachingAssistants: ITeachingAssistant[];
#   students: IStudent[];
# }


Student = namedtuple('Student', ['name', 'id', 'type'])
# interface IStudent extends IUser {}


TeachingAssistant = namedtuple(
    'TeachingAssistant', ['name', 'id', 'type', 'helping'])
# interface ITeachingAssistant extends IUser {
#   helping?: IStudent;
# }


class UserType(Enum):
    TeachingAssistant = "teaching_assistant",
    Student = "student"
# enum EUserType {
#   TeachingAssistant = "teaching_assistant",
#   Student = "student"
# }
