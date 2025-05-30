import reflex as rx

def robots():
    """Renderiza el robots.txt."""
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /login

Sitemap: https://tudominio.com/sitemap.xml"""
    
    return rx.text(content, content_type="text/plain") 