# Espacios de datos federados · datos.softwareinabox.eu

Web de la línea de **espacios de datos federados** de **Software in a Box** (https://www.softwareinabox.eu).

- Publicación: GitHub Pages (rama `main`) con dominio `datos.softwareinabox.eu`, detrás de Cloudflare.
- Primer vertical: espacio de datos dental con IA sobre Microsoft Azure (futuro subdominio healthdata.softwareinabox.eu).

## Idiomas
El español es la fuente (páginas de la raíz). Las versiones `/en/`, `/fr/`, `/de/`, `/nl/`, `/pt/` e `/it/` se generan con `i18n/build.py` a partir de `i18n/<idioma>.json`, y el mismo script añade hreflang, canonical, selector de idioma y `sitemap.xml`. Tras editar una página en español: `python3 i18n/build.py extract`, traducir los textos nuevos y `python3 i18n/build.py build`. No editar a mano las carpetas de idioma.

### Slugs traducidos
En `i18n/sites.json`, una página puede llevar `"paths": {"en": "/resources", ...}` con la ruta de cada idioma. `build.py` genera el fichero en esa ruta y deja en la ruta antigua (slug en español) una página de redirección con `noindex`. Hoy los usan `/recursos` y el artículo de geopolítica. Este cambio de `build.py` es compatible con las otras tres webs, pero de momento solo está en este repo.
