import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não esta definido nas variaveis de ambiente")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL não esta definido nas variaveis de ambiente")

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
if not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_ANON_KEY não esta definido nas variaveis de ambiente")
