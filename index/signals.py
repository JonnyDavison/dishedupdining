from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.apps import apps

@receiver(post_save)
def upload_to_s3(sender, instance, created, **kwargs):
    # Check if the model has any FileField or ImageField
    file_fields = [f for f in instance._meta.fields if f.get_internal_type() in ['FileField', 'ImageField']]
    
    for field in file_fields:
        file = getattr(instance, field.name)
        if file:
            file_name = file.name
            # Use default_storage to handle the file upload
            with file.open() as f:
                default_storage.save(file_name, f)
            print(f"File {file_name} uploaded to S3")
