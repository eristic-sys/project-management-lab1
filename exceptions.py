class ProjectManagementError(Exception):
    """Базовое исключение для системы управления проектами."""
    pass


class EntityNotFoundError(ProjectManagementError):
    """Исключение, возникающее, когда сущность не найдена."""
    pass


class ValidationError(ProjectManagementError):
    """Исключение для ошибок валидации данных."""
    pass