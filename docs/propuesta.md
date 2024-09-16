<p align="center">
Propuesta de Tesis de Licenciatura en Ciencias de la Computación
</p>
<p align="center">
Facultad de Matemática, Astronomía, Física y Computación
</p>
<p align="center">
Alumno: Gonzalo García Zurlo
</p>
<p align="center">
Director: Daniel Gutson
</p>
<p align="center">
Asistente de Dirección: Pedro D'Argenio
</p>


#### Título:
*Evaluación del "Delta Diseño" en Revisiones de Código para Controlar la Deuda Técnica en Entornos Ágiles*

#### Resumen:
Esta tesis propone el desarrollo de un sistema que evalúe los cambios de diseño implícitos en el código fuente durante las revisiones de código en entornos ágiles. El sistema comparará el diseño implícito en el código original con el diseño implícito en el código modificado. Si la diferencia entre ambos diseños supera un umbral determinado, el sistema detendrá el pipeline de CI y requerirá una revisión explícita del diseño. La propuesta incluye la creación de una función de distancia entre dos diseños orientados a objetos y un DSL para especificar las métricas de diseño. El proyecto se centrará en código escrito en Python, utilizando pyreverse para extraer el diseño a partir del código.

#### Planteamiento del Problema:
La transición del modelo Waterfall y el diseño extenso inicial (BDUF) hacia el Diseño Emergente en metodologías ágiles ha traído consigo una serie de desafíos. En muchos proyectos, el diseño emerge implícitamente a medida que avanza la programación, sin instancias formales de diseño previo (ni siquiera spikes). Esto puede llevar a que cambios importantes en el diseño pasen inadvertidos durante las revisiones de código, ya que los revisores pueden no percibir la magnitud del cambio de diseño que está ocurriendo implícitamente. Este fenómeno contribuye significativamente a la acumulación de deuda técnica, ya que el diseño puede divergir de forma no controlada en el apuro por cumplir con plazos y entregar nuevas funcionalidades.

#### Solución Propuesta:
Se propone un sistema que evalúe el "delta diseño" durante las revisiones de código, comparando el diseño implícito en el código original con el diseño implícito en el código modificado. La evaluación se realizará mediante una función de distancia entre diseños, que medirá diferencias en métricas clave, como el acoplamiento (coupling), cambios en la jerarquía de clases, entre otras. Cada una de estas diferencias será ponderada y elevada a una potencia específica para calcular la distancia total. Si la distancia supera un umbral predefinido, el sistema detendrá el pipeline de CI y requerirá una revisión explícita del diseño antes de continuar.

#### Diseño del Sistema:
1. *Función de Distancia:*
   - La función de distancia entre dos diseños se compondrá de varios deltas métricos, como el delta-coupling (cambio en el acoplamiento entre clases) y el delta de cambios en la jerarquía de clases (número de clases que cambiaron de clase base).
   - Cada delta será ponderado por un coeficiente específico y elevado a una potencia para determinar su impacto en la distancia total.
   - La suma ponderada de estos deltas definirá la distancia total entre los dos diseños.

2. *Lenguaje Específico de Dominio (DSL):*
   - Se diseñará un DSL para permitir la especificación de las métricas de diseño que serán utilizadas en la función de distancia.
   - El DSL será extensible, permitiendo a los usuarios definir nuevas métricas y ajustar los coeficientes y potencias según las necesidades específicas del proyecto.

3. *Extracción del Diseño:*
   - El proyecto se centrará en código escrito en Python.
   - Se utilizará la herramienta pyreverse para extraer el diseño del código fuente y generar diagramas UML en formato PlantUML.
   - El proyecto incluirá la implementación de un parser para analizar estos diagramas y extraer la información necesaria para la evaluación del delta diseño.

4. *Integración con CI:*
   - El sistema se integrará con pipelines de CI, deteniéndolos automáticamente si se detecta un cambio de diseño significativo, solicitando una revisión explícita del diseño antes de continuar.

#### Plan de Ejecución:

1. *Revisión de la Literatura:*
   - Investigar enfoques actuales para la evaluación de cambios de diseño en entornos ágiles.
   - Estudiar herramientas de análisis estático de código y técnicas de diseño emergente.

2. *Análisis de Requisitos:*
   - Definir las métricas de diseño que se utilizarán para calcular el delta diseño.
   - Especificar los coeficientes y potencias iniciales para la función de distancia.

3. *Diseño e Implementación:*
   - Desarrollar el DSL para la especificación de métricas de diseño.
   - Implementar la función de distancia y su integración con el sistema de CI.
   - Desarrollar el parser para analizar los diagramas generados por pyreverse.

4. *Pruebas y Validación:*
   - Evaluar el sistema en proyectos de software libre conocidos.
   - Recopilar estadísticas sobre las métricas y ajustar los coeficientes, potencias y umbral del delta diseño.
   - Comparar los resultados con revisiones de código tradicionales para validar la efectividad del sistema.

5. *Documentación y Reporte:*
   - Documentar el diseño, implementación y pruebas del sistema.
   - Preparar el informe final de la tesis, incluyendo conclusiones y recomendaciones para trabajos futuros.

#### Contribuciones Esperadas:
Esta tesis contribuirá con un sistema innovador para controlar los cambios de diseño implícitos en proyectos ágiles, ayudando a mitigar la acumulación de deuda técnica. El sistema permitirá a los equipos de desarrollo identificar y gestionar de manera proactiva cambios significativos en el diseño, asegurando una mayor calidad y sostenibilidad del código a largo plazo.


#### Bibliografía y Referencias
[1] Scott A. Whitmire. 1997. Object Oriented Design Measurement (1st. ed.). John Wiley & Sons, Inc., USA.
[2] Grady Booch, Robert Maksimchuk, Michael Engle, Bobbi Young, Jim Conallen, and Kelli Houston. 2007. Object-oriented analysis and design with applications, third edition (Third. ed.). Addison-Wesley Professional.
[3] Robert Cecil Martin. 2003. Agile Software Development: Principles, Patterns, and Practices. Prentice Hall PTR, USA.
[4] Robert C. Martin. 2017. Clean Architecture: A Craftsman's Guide to Software Structure and Design (1st. ed.). Prentice Hall Press, USA.
  