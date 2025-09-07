import supabase

from app.config.settings import settings

# Создаем единственный, глобальный экземпляр клиента Supabase
# Этот клиент будет переиспользоваться во всем приложении
supabase_client: supabase.Client = supabase.create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY,
)
