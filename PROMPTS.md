# Prompts Utilizados — Evaluación Técnica
## Cómo Usé la IA como Compañera de Sparring para Acelerar mi Pensamiento Arquitectónico

**Candidato:** Oscar Mauricio Vargas Arce  
**Cargo al que Aplico:** Tech Lead 
**Fecha de Evaluación:** Mayo 2026  
**Herramientas de IA Utilizadas:** 
- **Kimi K2.6 (Moonshot AI)** — Prompts principales, estructura del documento, 
  generación del framework de resiliencia y demo service.
- **Deepseek** — Investigación profunda sobre patrones de resiliencia, 
  comparación de estrategias de circuit breaker, y validación de decisiones arquitectónicas.
- **Claude (Anthropic)** — Revisión de calidad de código, refinamiento de ADRs, 
  y pulido de lenguaje técnico en inglés.

**Nota sobre múltiples herramientas:** Cada modelo tiene fortalezas distintas. 
Usar varios me permitió contrastar perspectivas, detectar inconsistencias, y 
tomar decisiones informadas. En todos los casos, **las decisiones finales fueron mías**.

---

## Mi Filosofía de Uso de la IA

Usé la IA como **compañera de sparring y aceleradora**, no como reemplazo de mi juicio técnico. Mi proceso siguió tres principios:

1. **Yo aporté el contexto** — Mis 9+ años de experiencia (Java, Python, Javascript, microservicios, ETL a escala, coordinación cross-team en Walmart y Claro) enmarcaron cada prompt.
2. **Yo establecí las restricciones** — Definí explícitamente el rol (Tech Lead, no arquitecto senior), la estructura del equipo (sin arquitecto dedicado, células multidisciplinarias), y el formato del entregable.
3. **Yo iteré y validé** — No acepté la primera respuesta. Cuestioné supuestos, pedí alternativas, y adapté el código para demostrar patrones que entendía conceptualmente pero quería validar prácticamente.

A continuación están los prompts reales que utilicé, organizados por sección de la evaluación.

---

## Sección A — Arquitectura y Roadmap

### Prompt 1: Establecer la Línea Base Arquitectónica

```
Soy un Tech Lead con 9 años de experiencia en Java, microservicios y pipelines ETL. 
He trabajado con microservicios en GCP y procesado +1 millón de registros diarios en 
sistemas CDR de telecomunicaciones, pero ahora estoy dando el paso hacia arquitectura 
para un Canal Digital Directo multi-país.

Necesito diseñar una arquitectura target end-to-end que sea:
- Alta disponibilidad y multi-región
- Escalable a millones de usuarios
- Resiliente ante fallos de servicios upstream
- Observable y operacionalmente madura

Mi equipo no tiene arquitecto dedicado. Yo seré el punto de contacto técnico entre 
células multidisciplinarias que rotan miembros. Necesito una 
arquitectura que las células puedan construir de forma autónoma pero consistente.

Por favor ayúdame a estructurar:
1. Las capas de arquitectura (Edge, Aplicación, Integración, Datos, Observabilidad, Seguridad)
2. Cómo encajan los patrones de resiliencia (retries, circuit breaker, idempotencia, 
   bulkheads, mensajería async, caché) en cada capa
3. Un roadmap realista de 12 semanas dividido en 3 workstreams: Confiabilidad, 
   Modernización de Integración, y Observabilidad/Operaciones

Responde en inglés. Sé específico sobre trade-offs. No asumas que soy arquitecto senior — 
señala las áreas donde necesito validación más profunda.
```

### Prompt 2: Refinar el Roadmap para Mi Contexto Real

```
El roadmap que me diste está bien, pero necesito adaptarlo a mi realidad:
- Trabajo en ambiente Scrum y yo mismo creo las historias de usuario
- Necesito coordinar células que no siempre tienen los mismos miembros
- Tengo experiencia con ETL batch (SSIS) pero estoy aprendiendo arquitectura orientada a eventos
- Mi área más fuerte es procesamiento de datos e integración; mi más débil es 
  despliegue multi-región global

Por favor revisa el roadmap de 12 semanas para:
1. Reflejar el alcance de un Tech Lead (no de un CTO)
2. Incluir hitos de aprendizaje donde reconozco brechas
3. Mostrar cómo el workstream de Integración se construye sobre mi experiencia ETL
4. Hacer Observabilidad realista para alguien que ha usado Power BI/SSIS monitoring 
   pero no distributed tracing
```

### Prompt 3: Descripción del Diagrama de Arquitectura

```
Necesito describir un diagrama de arquitectura para un canal digital multi-región, 
pero no soy experto en visualización. Ayúdame a definir:

1. Qué zonas debe tener el diagrama (arriba, centro, abajo, izquierda, derecha)
2. Qué iconos y codificación de colores usar
3. Qué representan los estilos de línea (sync vs async, límites de circuito, capas de caché)
4. Tres niveles de zoom: Contexto del Sistema, Contenedores, y Detalle de Componentes

Manténlo práctico — algo que pueda dibujar en Draw.io en 2 horas.
```

---

## Sección B — Framework de Integración Reutilizable

### Prompt 4: Principios de Diseño del Framework

```
Necesito diseñar un framework de integración reutilizable en Python que demuestre 
patrones de resiliencia enterprise-grade. Es para una evaluación técnica, así que 
necesita ser ejecutable y educativo.

El framework debe incluir:
1. Timeouts y retries con exponential backoff + jitter
2. Circuit breaker con estados CLOSED/OPEN/HALF_OPEN
3. Configuración centralizada (ResilienceConfig)
4. Logging estructurado unificado con propagación de trazas
5. Propagación de trazas estilo OpenTelemetry (simplificado, compliant W3C)
6. Soporte para claves de idempotencia

He usado Spring Boot con Hystrix antes, así que entiendo circuit breakers conceptualmente. 
También he implementado retry logic en pipelines ETL. Pero quiero construir esto desde 
cero en Python para probar que entiendo los internals — no solo cómo usar una librería.

Por favor proporciona:
- Un diseño modular con separación clara de responsabilidades
- Decisiones de diseño explicadas (¿por qué full jitter? ¿por qué HALF_OPEN? 
  ¿por qué circuit breakers por destino?)
- Código realista para producción pero legible para propósitos de evaluación
- Notas honestas sobre qué está simplificado vs qué sería production-grade
```

### Prompt 5: Revisión de Código e Iteración

```
El código del framework se ve bien, pero quiero validar algunas decisiones:

1. Usé threading.Lock para thread safety. ¿Es esto suficiente para un demo, 
   o debería usar asyncio/patrones reactivos? Quiero ser honesto de que esto 
   es una implementación simplificada.

2. El idempotency store está en memoria. Sé que producción necesita Redis Cluster. 
   ¿Cómo documento esta brecha sin hacer que el demo falle?

3. ¿Puedes agregar comentarios honestos de "Design Decision" en el código que 
   expliquen los trade-offs? Esto demuestra que entiendo consecuencias, no solo sintaxis.

4. Agrega excepciones personalizadas (CircuitBreakerOpenException, BulkheadFullException, etc.) 
   para que el demo service pueda capturarlas gracefulmente.
```

---

## Sección C — Servicio Demo y Test de Confiabilidad

### Prompt 6: Diseñar el Simulador de Upstream Inestable

```
Necesito construir un servicio demo que use mi framework de integración para llamar 
a un payment gateway upstream inestable. El upstream debe simular modos de fallo del mundo real:

- 60% errores de servidor (500, 502, 503, 504)
- 20% timeouts (requests se cuelgan más allá del timeout)
- 20% éxitos lentos (tiempo de respuesta 0.5-2.5s)

El demo debe ejecutar 6 tests:
1. Llamadas secuenciales mostrando retries con backoff
2. Apertura del circuit breaker después del umbral
3. Fast-fail cuando el circuito está OPEN
4. Recuperación del circuito (HALF_OPEN -> CLOSED)
5. Idempotencia (request duplicado devuelve respuesta cacheada)
6. Saturación del bulkhead bajo carga concurrente

Tengo experiencia con Python y threading de mentorizar 500+ desarrolladores en 
bootcamps MinTIC/SENA. Haz el código limpio y bien comentado.
```

### Prompt 7: Hacer el Demo Ejecutable y Entendible

```
El demo funciona, pero necesito asegurarme de que sea fácil de ejecutar para los evaluadores. 
Por favor:

1. Agrega print statements claros mostrando qué hace cada test
2. Muestra las transiciones de estado del circuit breaker en la salida
3. Agrega un resumen al final listando qué patrones fueron demostrados
4. Asegúrate de que el demo complete en menos de 2 minutos (ajusta timeouts/sleep)
5. Agrega comentarios explicando qué prueba cada test conceptualmente
```

---

## Sección D — Registro de Decisiones Técnicas (ADR)

### Prompt 8: Estructura de ADR y Primera Decisión

```
Necesito escribir dos ADRs de una página comparando alternativas arquitectónicas. 
Nunca he escrito un ADR formal antes, pero entiendo análisis de trade-offs de mi 
trabajo como Business Analyst en Walmart CAM.

El formato debe ser: Contexto, Opciones, Decisión, Consecuencias.

ADR-001: Plataforma de Integración Centralizada vs Integraciones Descentralizadas 
          Propiedad de los Equipos
- Contexto: 40+ sistemas upstream, células multidisciplinarias, sin arquitecto dedicado
- Mi experiencia: En Walmart coordiné equipos Web/Core/App. En Claro trabajé dentro 
  de un modelo de integración de datos centralizado. He visto tanto fricción como consistencia.

Por favor ayúdame a estructurar esto honestamente:
- No me hagas sonar como si hubiera operado una plataforma de 40 integraciones antes
- Muestra que entiendo la Ley de Conway y la autonomía de equipos
- Propón un híbrido (Federado con Guardrails) pero márcalo como tentativo
```

### Prompt 9: Segundo ADR — Event-Driven vs Síncrono

```
ADR-002: Arquitectura Orientada a Eventos vs Solicitud-Respuesta Síncrona 
          para Flujos Críticos

Contexto: Pagos, apertura de cuenta, préstamos — deben ser confiables, auditables, recuperables.

Mi experiencia:
- En Claro, el procesamiento CDR era batch ETL. Funcionaba pero tenía puntos ciegos.
- En Universidad del Norte, los delays de batch hacían imposibles dashboards en tiempo real.
- Entiendo la teoría de CQRS, Saga y Event Sourcing de lectura, pero no los he 
  implementado en producción.

Ayúdame a escribir un ADR que:
1. Proponga un híbrido (CQRS + Saga) pero sea honesto sobre mis brechas
2. Liste preguntas específicas donde necesito mentoría (eventos huérfanos, 
   evolución de esquemas, lag de consumidores)
3. Muestre que entiendo el impacto de negocio (auditabilidad, latencia, experiencia de usuario)
4. Use el formato estándar de ADR
```

---

## Meta-Prompts: Tono y Posicionamiento

### Prompt 10: Establecer el Tono Correcto

```
Estoy completando esta evaluación para un cargo de Tech Lead. NO soy un arquitecto 
senior con 15 años de experiencia en sistemas distribuidos. Soy un ingeniero experimentado 
(9 años, Java, Python, Javascript, microservicios, ETL, liderazgo de equipos) haciendo una transición deliberada 
hacia arquitectura y propiedad técnica cross-celda.

Por favor ayúdame a reescribir el tono de todo el documento para reflejar esto:
- Confianza en lo que he construido y liderado
- Honestidad sobre lo que estoy aprendiendo
- Curiosidad y hambre de mentoría
- Pensamiento estratégico pero humildad sobre mis brechas de experiencia
- Profesionalismo y credibilidad técnica

El tono debe decir: "Traigo bases sólidas, ejecución probada, y una trayectoria de 
crecimiento clara. Estoy listo para aprender bajo guía experimentada."
```

### Prompt 11: Pulido Final y Consistencia

```
Por favor revisa el documento completo para:
1. Consistencia entre secciones (¿la Sección B referencia decisiones de la Sección A?)
2. Chequeos de honestidad (¿hay afirmaciones que exageren mi experiencia?)
3. Precisión técnica (¿los patrones de resiliencia están descritos correctamente?)
4. Calidad de lenguaje (inglés profesional, oraciones claras, sin relleno)
5. Alineación con mi experiencia (¿referencia Claro, Walmart, Movilplata, Universidad del Norte 
   donde sea apropiado?)

Señala cualquier cosa que suene como que estoy fingiendo ser experto cuando no lo soy.
```
### Prompt 12: Revisión de Calidad de Código con Claude

```
Actúa como un Senior Technical Reviewer con experiencia en sistemas
distribuidos y patrones de resiliencia en Python.
Tengo dos archivos que forman parte de una evaluación técnica para un
cargo de Tech Lead:

1. integration_framework.py — Framework de resiliencia reutilizable con:
  - Retry con exponential backoff + full jitter
  - Circuit Breaker (CLOSED/OPEN/HALF_OPEN)
  - Bulkhead con queue
  - IdempotencyStore con TTL
  - Propagación de trazas W3C simplificada
  - Logging estructurado con Trace ID

2. demo_service.py — Servicio demo que simula un payment gateway
inestable (60% errores, 20% timeouts) y ejecuta 6 tests de
confiabilidad contra el framework.

Por favor evalúa ambos archivos bajo estos criterios:

1. SOLID y Clean Code: ¿Las responsabilidades están bien separadas?
¿Hay acoplamiento innecesario? ¿Los nombres son expresivos?
2. Mantenibilidad: ¿Puede un equipo con niveles mixtos mantener este código sin documentación adicional?
3. Thread safety: ¿El uso de threading.Lock es suficiente para
el propósito del demo? ¿Qué riesgos tiene en producción?
4. Deuda técnica honesta: ¿Qué simplificaciones del demo
serían bloqueantes en producción? Sé específico.
5. Lo que NO debes hacer: No sugieras reescribir el framework
completo ni agregues dependencias externas. El objetivo es que corra con Python estándar.

Formato de respuesta:

Fortalezas concretas (con referencias a líneas o clases específicas)
Deuda técnica identificada (con impacto estimado)
Máximo 3 mejoras puntuales que pueda aplicar en 30 minutos
Veredicto: ¿Es código defendible en una entrevista técnica?
``
```
---

## Lo Que NO Hice con la IA

Para ser completamente transparente, esto es lo que hice manualmente:

- **Ejecutar el código:** Corrí `python demo_service.py` en mi máquina local y 
  validé la salida yo mismo.
- **Decisiones de arquitectura:** Proporcioné mis experiencias reales (fricción cross-team 
  en Walmart, limitaciones de batch en Claro) como restricciones. La IA ayudó a estructurarlas, 
  pero el contexto fue mío.
- **Adaptación de código:** Modifiqué valores de timeout, tasas de fallo, y límites de 
  bulkhead para hacer que el demo corriera en menos de 2 minutos.
- **Calibración de tono:** Rechacé el primer borrador porque sonaba demasiado senior. 
  Pedí explícitamente a la IA que reposicionara el tono a mi nivel real.

---

## Estructura del Repositorio

```
demo-resiliencia/
├── integration_framework.py      # Framework de resiliencia reutilizable
├── demo_service.py               # Servicio demo con 6 tests de confiabilidad
├── PROMPTS.md                    # Este archivo — transparencia en uso de IA
├── README.md                     # Cómo ejecutar el demo (inglés)
└── assessment-document.md        # Evaluación técnica completa (Secciones A-D)
```

---

## Reflexión Final

Usar IA para esta evaluación me permitió:
- **Acelerar investigación** sobre patrones que conocía conceptualmente pero quería validar a profundidad
- **Validar implementaciones** comparando mi modelo mental con código generado
- **Estructurar argumentos complejos** (ADRs, análisis de trade-offs) usando frameworks que estaba aprendiendo
- **Mantener honestidad** al señalar explícitamente brechas de experiencia en lugar de ocultarlas

Lo que la IA NO hizo:
- Reemplazar mi juicio técnico
- Inventar experiencias que no tengo
- Tomar decisiones arquitectónicas que yo no asumí
- Correr o probar el código

Creo que esta es la forma correcta de usar IA en evaluaciones técnicas: como un 
multiplicador de fuerza para ingenieros capaces, no como una muleta para quienes 
carecen de fundamentos.

---

**Oscar Mauricio Vargas Arce**  
Tech Lead | Business Analyst | Arquitecto en Formación
