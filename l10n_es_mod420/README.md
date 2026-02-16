# España - Informe Fiscal Mod 420 (IGIC Islas Canarias)

## Descripción

Este módulo proporciona el Informe Fiscal Oficial Español Mod 420 para las Islas Canarias, que maneja el IGIC (Impuesto General Indirecto Canario) en lugar del IVA regular.

### Características

- ✅ **Informe completo de IGIC (Mod 420)** con todas las secciones requeridas
- ✅ **Etiquetas fiscales** para categorización adecuada (mod420[1] hasta mod420[45])
- ✅ **Plantillas fiscales específicas de Canarias** para todos los tipos de IGIC
- ✅ **Soporte para todos los tipos de IGIC**: 0%, 3%, 5%, 7%, 9.5%, 15%, 20%
- ✅ **Manejo de bienes de inversión** (secciones 28-29, 32-33)
- ✅ **Soporte para operaciones de importación** (secciones 30-31, 32-33)
- ✅ **Secciones de correcciones y ajustes** (21-22, 34-35)
- ✅ **Campos de entrada manual** para casos especiales (36-39, 42-44)
- ✅ **Cálculos automáticos** para totales y diferencias

### ¿Qué es el IGIC?

El IGIC (Impuesto General Indirecto Canario) es el impuesto indirecto que se aplica en las Islas Canarias en lugar del IVA español. El Mod 420 es el formulario de declaración trimestral para este impuesto.

### Migración desde Odoo 18

Este módulo es una migración limpia de la funcionalidad del Mod 420 desde el módulo `l10n_es` de Odoo 18, específicamente adaptado para entornos de Odoo 17 que necesitan únicamente este informe.

**Importante**: Este módulo proporciona únicamente la **estructura del informe** y las **etiquetas fiscales**. Necesitas asignar manualmente las etiquetas a tus impuestos IGIC existentes o usar el módulo OCA `l10n_es_igic` para una configuración completa del IGIC.

### Uso

1. Instalar el módulo
2. Ir a Contabilidad > Informes > Informes Fiscales
3. Seleccionar "Informe Fiscal (Mod 420) Islas Canarias"
4. Configurar el rango de fechas y generar el informe
5. **Configurar tus impuestos IGIC** para usar las etiquetas mod420 proporcionadas para una categorización adecuada

### Etiquetas Fiscales Disponibles

El módulo proporciona todas las etiquetas fiscales necesarias:
- `+mod420[1]` hasta `+mod420[35]` para diferentes operaciones fiscales
- `-mod420[21]`, `-mod420[22]`, etc. para devoluciones y correcciones

### Detalles Técnicos

- **País**: España (ES)
- **Sistema Fiscal**: IGIC (Islas Canarias)
- **Tipo de Informe**: Declaración fiscal trimestral
- **Versión de Odoo**: 17.0
- **Dependencias**: account, base, l10n_es
- **Idiomas**: Español (es), Inglés (en)
- **Traducciones**: Archivos de traducción completos incluidos

### Instalación

1. Copiar este módulo al directorio de addons de Odoo
2. Actualizar la lista de módulos
3. Instalar el módulo desde el menú Aplicaciones
4. Configurar tus impuestos IGIC para usar las etiquetas mod420

### Configuración Recomendada

Para una configuración completa del IGIC, considera también instalar:
- Módulo OCA `l10n_es_igic` para impuestos IGIC
- Este módulo para informes Mod 420

### Autor

**NextaDS**
- Sitio web: https://www.nextads.es