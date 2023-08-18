from django.core.validators import (
    get_available_image_extensions,
    FileExtensionValidator,
)


def validate_image_and_svg_file_extension(value):
    allowed_extensions = get_available_image_extensions()
    allowed_extensions.append("svg")
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)
