from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_size(value):
    filesize = value.size
    
    if filesize > 10 * 1024 * 1024:  # 10MB limit
        raise ValidationError(_("The maximum file size that can be uploaded is 10MB"))
    else:
        return value