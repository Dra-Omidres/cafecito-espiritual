# Cafecito Espiritual — videos multired

## Estado
Implementación técnica inicial instalada en GitHub; verificar el resultado de la acción `Cafecito - Render multired vertical` antes de declarar el sistema en producción.

## Objetivo
Un solo archivo MP4 vertical **1080×1920 (9:16)** para reutilizar, con publicaciones independientes, en:
- YouTube Shorts: título, descripción, público general (`madeForKids:false`).
- Instagram Stories: `instagramData.type = STORY`. La historia no admite copy visible como pie de publicación.
- Facebook Stories: `facebookData.type = STORY`.
- Opcionales: Reels de Instagram y Facebook (`REEL`).

## Flujo
1. ChatGPT verifica fuentes católicas y prepara oración, texto, imagen PNG/JPG.
2. Guarda la imagen en `imagenes/` (no incluir archivos privados).
3. Crea un archivo `solicitudes-video/<id>.json` con el manifiesto de producción.
4. GitHub Actions ejecuta `.github/workflows/render-multired.yml`, que invoca `scripts/render_multired.py`.
5. Confirma que existen `videos/<id>.mp4` y `videos/<id>.json`.
6. Antes de programar, valida el archivo MP4 desde el enlace RAW público y revisa Metricool para evitar duplicados.
7. Agenda **publicaciones separadas** en Metricool, marca **7517190**, zona `America/Guayaquil`, con `autoPublish:true` y `draft:false`.
8. Reporta `PENDING` mientras esté programado y `PUBLISHED` solo cuando se confirme realmente.

## Ejemplo de manifiesto
```json
{
  "id": "oracion-2026-10-21",
  "imagen": "imagenes/oracion-2026-10-21.png",
  "duracion": 12,
  "titulo": "Una oración para comenzar el día | Cafecito Espiritual",
  "referencia": "Salmo 23,1",
  "publicar": true
}
```

El nombre `id` debe ser único; la imagen indicada debe existir antes de crear el manifiesto. El manifiesto de **prueba-tecnica-multired-2026-10-20** tiene `publicar:false` y no debe programarse.

## Política musical
**Preferencia:** canto gregoriano auténtico en latín; segunda opción música sacra instrumental; tercera canto devocional sobrio en español. Solo usar grabaciones autorizadas/licenciadas para publicación multiplataforma. Si se utiliza música, añadir al manifiesto tanto `audio` como `licencia_audio`, apuntando a archivos existentes en el repositorio. El render falla si falta la constancia de licencia.

Sin archivos musicales autorizados, se genera un video silencioso. No se insertará música comercial ni canto grabado con derechos no verificados. Este proceso básico usa movimiento/fundidos sobre una imagen; no equivale a una generación cinematográfica en Higgsfield.

## Control de calidad
Verificar ortografía, cita bíblica, encuadre 9:16, legibilidad, logo discreto, duración 6-30 s, licencia del audio, calidad del MP4, conexión de cada red, ausencia de duplicados y estados retornados por Metricool.

## Limitaciones actuales
No se ha confirmado aún la primera ejecución exitosa del workflow multired. Además, Metricool y GitHub deben seguir conectados y autorizados. La publicación automática depende de la aceptación de cada plataforma y de archivos públicamente accesibles.
