from supabase import create_client, Client
import os
from app.core.config import settings

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)