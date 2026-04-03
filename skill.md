# 🧠 Skill: Análisis de Requerimientos para Proyectos Full Stack

## 📌 ¿Qué es el Análisis de Requerimientos?

El **análisis de requerimientos** es el proceso de identificar, documentar y gestionar las necesidades y expectativas de los interesados (stakeholders) antes de desarrollar un sistema de software. Es una de las etapas más críticas en el ciclo de vida del desarrollo de software, ya que los errores cometidos aquí se propagan y amplifican en todas las fases posteriores.

En proyectos **full stack**, este análisis debe contemplar tanto la capa del cliente (frontend) como la del servidor (backend), la base de datos y las integraciones con servicios externos.

---

## 🎯 Resumen de Skills Involucrados

| Skill | Descripción breve |
|---|---|
| **Levantamiento de requerimientos** | Técnica para recopilar información con stakeholders mediante entrevistas, talleres o encuestas |
| **Modelado de casos de uso** | Representación visual de las interacciones entre actores y el sistema |
| **Priorización (MoSCoW)** | Clasificación de requerimientos en Must, Should, Could y Won't have |
| **Gestión de backlog** | Organización y seguimiento de requerimientos en herramientas como Jira o Trello |
| **Documentación técnica** | Redacción clara de especificaciones para equipos de desarrollo y diseño |
| **Pensamiento crítico** | Detectar ambigüedades, contradicciones o vacíos en los requerimientos levantados |

---

## ✅ Requerimientos Funcionales

Los **requerimientos funcionales** describen **qué debe hacer** el sistema: las funciones, comportamientos y características que el software debe proveer a sus usuarios.

### Cómo aplicar el skill al análisis funcional

1. **Identificar actores y roles**: Determinar quiénes usarán el sistema (ej. usuario final, administrador, sistema externo).
2. **Definir casos de uso**: Por cada actor, listar las acciones que puede realizar dentro del sistema.
3. **Redactar historias de usuario**: Usar el formato `Como [rol], quiero [acción] para [beneficio]`.
4. **Establecer criterios de aceptación**: Condiciones concretas y verificables que deben cumplirse para dar un requerimiento por completado.
5. **Priorizar con MoSCoW**: Distinguir qué funcionalidades son esenciales del MVP y cuáles pueden diferirse.

### Ejemplo aplicado a un proyecto full stack (Sistema de Parqueo)

| ID | Historia de usuario | Criterio de aceptación | Prioridad |
|---|---|---|---|
| RF-01 | Como conductor, quiero registrar mi vehículo en el parqueo para asegurar un espacio | El sistema asigna un espacio disponible y devuelve un ticket con ID y hora de entrada | Must |
| RF-02 | Como conductor, quiero retirar mi vehículo para pagar y salir del parqueo | El sistema calcula el cobro según tiempo transcurrido y libera el espacio | Must |
| RF-03 | Como administrador, quiero ver la ocupación en tiempo real para gestionar el espacio | El panel muestra espacios libres y ocupados actualizados | Should |
| RF-04 | Como administrador, quiero exportar reportes de uso diario para análisis de datos | El sistema genera un archivo CSV con registros del día | Could |

---

## 🔒 Requerimientos No Funcionales

Los **requerimientos no funcionales** describen **cómo debe comportarse** el sistema: sus atributos de calidad, restricciones y características operativas que no están relacionadas directamente con una función específica.

### Categorías principales

| Categoría | Descripción |
|---|---|
| **Rendimiento** | Tiempo de respuesta, throughput, manejo de carga |
| **Seguridad** | Autenticación, autorización, cifrado, protección de datos |
| **Disponibilidad** | Uptime esperado, tolerancia a fallos, recuperación ante desastres |
| **Escalabilidad** | Capacidad de crecer horizontal o verticalmente ante mayor demanda |
| **Usabilidad** | Facilidad de uso, accesibilidad, curva de aprendizaje |
| **Mantenibilidad** | Legibilidad del código, modularidad, facilidad de actualización |
| **Portabilidad** | Compatibilidad con navegadores, sistemas operativos, dispositivos |

### Cómo aplicar el skill al análisis no funcional

1. **Recopilar restricciones del negocio y técnicas**: ¿Hay acuerdos de nivel de servicio (SLA)? ¿Regulaciones legales (GDPR, HIPAA)?
2. **Establecer métricas medibles**: Un requerimiento no funcional debe poder verificarse (ej. "el sistema debe responder en menos de 2 segundos bajo carga de 100 usuarios concurrentes").
3. **Vincular a decisiones de arquitectura**: Cada requerimiento no funcional tiene impacto en las decisiones de diseño del stack.
4. **Revisar con el equipo de infraestructura y seguridad**: No solo los desarrolladores deben conocer estos requerimientos.

### Ejemplo aplicado a un proyecto full stack (Sistema de Parqueo)

| ID | Requerimiento | Métrica / Condición | Categoría |
|---|---|---|---|
| RNF-01 | El sistema debe responder a las solicitudes de registro en menos de 2 segundos | Prueba de carga con 50 usuarios simultáneos | Rendimiento |
| RNF-02 | Los datos de pago deben transmitirse cifrados | Uso de HTTPS/TLS 1.2 o superior en todas las transacciones | Seguridad |
| RNF-03 | El sistema debe estar disponible el 99.5% del tiempo mensual | Monitoreo continuo con alertas automáticas | Disponibilidad |
| RNF-04 | La interfaz debe ser responsiva y funcionar en Chrome, Firefox y Safari | Pruebas cross-browser en las 3 últimas versiones de cada navegador | Portabilidad |
| RNF-05 | El código debe seguir estándares de estilo definidos y contar con cobertura de pruebas ≥ 80% | Análisis estático con linter y reporte de cobertura en CI/CD | Mantenibilidad |

---

## 🔄 Integración del Análisis en el Proyecto Full Stack

```
Stakeholders
     │
     ▼
Levantamiento de requerimientos (entrevistas, talleres)
     │
     ▼
Clasificación: Funcionales vs No Funcionales
     │
     ├──────────────────────────────────┐
     ▼                                  ▼
Historias de usuario            Atributos de calidad
Casos de uso                    Restricciones técnicas
Criterios de aceptación         Métricas verificables
     │                                  │
     └──────────────┬───────────────────┘
                    ▼
           Backlog priorizado (MoSCoW)
                    │
                    ▼
     ┌──────────────┴──────────────────┐
     ▼                                 ▼
 Backend (API, DB, servicios)    Frontend (UI, UX, accesibilidad)
```

### Consideraciones específicas para un stack full stack

- **Frontend**: Los requerimientos funcionales definen las pantallas, flujos y validaciones del lado del cliente. Los no funcionales exigen accesibilidad (WCAG), rendimiento de carga (LCP < 2.5s) y compatibilidad.
- **Backend**: Los requerimientos funcionales especifican los endpoints de la API, reglas de negocio y lógica de datos. Los no funcionales dictan seguridad de la API (JWT, OAuth), tiempo de respuesta y manejo de errores.
- **Base de datos**: Los requerimientos funcionales determinan el modelo de datos. Los no funcionales exigen integridad referencial, respaldos automáticos y tiempos de consulta.

---

## 📚 Herramientas Recomendadas

| Herramienta | Uso en análisis de requerimientos |
|---|---|
| **Jira / Trello** | Gestión del backlog y seguimiento de historias de usuario |
| **Confluence / Notion** | Documentación centralizada de requerimientos |
| **Figma** | Prototipado para validar requerimientos funcionales de UI |
| **Miro / Lucidchart** | Diagramas de casos de uso y flujos del sistema |
| **Postman** | Definición y validación de contratos de API (requerimientos de backend) |

---

## 💡 Conclusión

El análisis de requerimientos es el **cimiento de cualquier proyecto full stack exitoso**. Aplicar correctamente las habilidades de levantamiento, clasificación, documentación y priorización de requerimientos:

- Reduce el riesgo de retrabajo costoso en etapas avanzadas del proyecto.
- Alinea al equipo técnico con los objetivos del negocio.
- Permite establecer un contrato claro entre desarrolladores, diseñadores y stakeholders.
- Garantiza que tanto los aspectos funcionales (qué hace el sistema) como los no funcionales (cómo se comporta) estén cubiertos desde el inicio.

> _"Un requerimiento bien definido hoy ahorra semanas de correcciones mañana."_
