import os
from django.core.files.storage import Storage
from django.conf import settings
from django.core.files.base import ContentFile
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "uploads") 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseStorage(Storage):
    def _open(self, name, mode='rb'):
        bucket = supabase.storage.from_(SUPABASE_BUCKET)
        response = bucket.download(name)
        return ContentFile(response)

    def _save(self, name, content):
        file_data = content.read()
        bucket = supabase.storage.from_(SUPABASE_BUCKET)

        # Make sure the path is unique if needed
        res = bucket.upload(path=name, file=file_data, file_options={"content-type": content.content_type})

        if res.get("error"):
            raise Exception(f"Supabase upload error: {res['error']['message']}")

        return name

    def delete(self, name):
        bucket = supabase.storage.from_(SUPABASE_BUCKET)
        bucket.remove([name])

    def exists(self, name):
        bucket = supabase.storage.from_(SUPABASE_BUCKET)
        res = bucket.list()
        return any(obj['name'] == name for obj in res['data'])

    def url(self, name):
        bucket = supabase.storage.from_(SUPABASE_BUCKET)
        public_url = bucket.get_public_url(name)
        return public_url['publicURL'] if isinstance(public_url, dict) else public_url
