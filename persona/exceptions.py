from rest_framework import exceptions, status


class PersonalInfoAlreadyExists(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Personal info already exists."
    default_code = "conflict"
