import reflex as rx
from ..models.blog import BlogPost
from datetime import datetime

def generate_sitemap():
    """Genera el sitemap.xml con las URLs del sitio."""
    # URLs estáticas
    urls = [
        "/",
        "/quien-soy",
        "/proyectos",
        "/blog",
        "/contacto",
    ]
    
    # URLs dinámicas del blog
    blog_posts = BlogPost.select()
    for post in blog_posts:
        urls.append(f"/blog/{post.slug}")
    
    # Generar el XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>https://tudominio.com{url}</loc>\n'
        xml += '    <lastmod>' + datetime.now().strftime("%Y-%m-%d") + '</lastmod>\n'
        xml += '    <changefreq>weekly</changefreq>\n'
        xml += '    <priority>0.8</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return xml

def sitemap():
    """Renderiza el sitemap.xml."""
    return rx.text(generate_sitemap(), content_type="application/xml") 