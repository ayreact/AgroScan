# your_app/fields.py
import os
from django.db.models.fields.files import FileField
from django.conf import settings
from django.core.files.storage import default_storage
from supabase import create_client
from urllib.parse import urlparse

class SupabaseStorage:
    def __init__(self, bucket_name=None):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.client = create_client(self.supabase_url, self.supabase_key)
        self.bucket_name = bucket_name if bucket_name else self._get_default_bucket_name()

    def _get_default_bucket_name(self):
        return getattr(settings, 'SUPABASE_BUCKET', 'default') # Using SUPABASE_BUCKET

    def _normalize_path(self, name):
        return name.replace('\\', '/')

    def save(self, name, content, max_length=None):
        name = self._normalize_path(name)
        try:
            self.client.storage.from_(self.bucket_name).upload(path=name, file=content.read())
            url = self.client.storage.from_(self.bucket_name).get_public_url(name)
            return url
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
            return None

    def delete(self, name):
        if not name:
            return
        try:
            path = urlparse(name).path.lstrip('/')
            self.client.storage.from_(self.bucket_name).remove(paths=[path])
        except Exception as e:
            print(f"Error deleting from Supabase: {e}")

    def url(self, name):
        if not name:
            return ''
        return name # Assuming save returns the full public URL

    def exists(self, name):
        try:
            path = urlparse(name).path.lstrip('/')
            response = self.client.storage.from_(self.bucket_name).list(path=os.path.dirname(path))
            for item in response:
                if item['name'] == os.path.basename(path):
                    return True
            return False
        except Exception as e:
            print(f"Error checking existence in Supabase: {e}")
            return False

    def size(self, name):
        # Supabase storage doesn't directly provide a simple way to get file size
        # without downloading the file or using database metadata if you store it.
        # This is a simplified return. You might need a more robust solution
        # depending on your requirements (e.g., storing size in your Django model).
        return 0

    def open(self, name, mode='rb'):
        # Opening a file for reading would typically involve downloading it.
        # This is a simplified implementation and might not be suitable for all use cases.
        try:
            path = urlparse(name).path.lstrip('/')
            res = self.client.storage.from_(self.bucket_name).download(path)
            if res.error:
                print(f"Error downloading from Supabase: {res.error}")
                return None
            from io import BytesIO
            return BytesIO(res.data)
        except Exception as e:
            print(f"Error opening file from Supabase: {e}")
            return None

class SupabaseFileField(FileField):
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        if storage is None:
            storage = SupabaseStorage(bucket_name=self._get_bucket_name_from_upload_to(upload_to))
        super().__init__(verbose_name, name, storage, **kwargs)
        self.upload_to = upload_to

    def _get_bucket_name_from_upload_to(self, upload_to):
        return getattr(settings, 'SUPABASE_BUCKET', 'default') # Using SUPABASE_BUCKET

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if isinstance(self.storage, SupabaseStorage):
            kwargs['storage'] = None
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        print("--- pre_save CALLED ---")
        file = super().pre_save(model_instance, add)
        print(f"File object: {file}")
        current_value = getattr(model_instance, self.name)
        print(f"Current value of image field: {current_value}")

        if file:
            print("A new file is being processed.")
            filename = file.name
            supabase_path = f"{self.upload_to}{filename}" # Construct the full Supabase path here
            url = self.storage.save(supabase_path, file) # Pass the full path to save
            print(f"Supabase URL: {url}")
            if url:
                setattr(model_instance, self.name, url)
                print(f"Image field set to: {getattr(model_instance, self.name)}")
            else:
                print("Supabase upload failed.")
            return None
        elif current_value and not isinstance(current_value, str) and hasattr(current_value, 'url'):
            print("Current value is a FieldFile.")
            if not self.storage.exists(current_value.url):
                print(f"File at {current_value.url} does not exist in Supabase. Clearing field.")
                setattr(model_instance, self.name, '')
        elif current_value and isinstance(current_value, str) and not self.storage.exists(current_value):
            print(f"URL {current_value} in database does not exist in Supabase. Clearing field.")
            setattr(model_instance, self.name, '')
        else:
            print("No new file, and current value exists or is None.")

        print("--- pre_save END ---")
        return file

    def save_form_data(self, instance, data):
        if data is not None:
            # If data is a File object (new upload)
            if hasattr(data, 'read'):
                url = self.storage.save(self.upload_to + data.name, data)
                if url:
                    setattr(instance, self.name, url)
            # If data is a string (existing URL, no new upload)
            elif isinstance(data, str):
                setattr(instance, self.name, data)
            # If data is False (field cleared)
            elif data is False:
                old_value = getattr(instance, self.name)
                if old_value:
                    self.storage.delete(old_value)
                setattr(instance, self.name, '')

    def delete(self, instance, keep_parents=False):
        value = getattr(instance, self.name)
        if value:
            self.storage.delete(value)
        super().delete(instance, keep_parents)

try:
    # Register the custom storage backend if you want to use it directly
    default_storage.register('supabase_storage', SupabaseStorage)
except AttributeError:
    pass