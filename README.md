# Chatbot para Automatización de Ventas de Quiniela v1.0
Este repositorio alberga el código fuente y la documentación del proyecto "Chatbot para Automatización de Ventas de Quiniela". El objetivo principal de este proyecto es proporcionar una herramienta automatizada para gestionar las ventas de una agencia de quiniela a través de mensajes de texto, utilizando la plataforma de mensajería Telegram.
## Características Principales
**Interfaz de Chatbot en Telegram**: El chatbot interactúa con los clientes de la agencia de quiniela a través de mensajes de texto en Telegram, respondiendo consultas y tomando pedidos de boletos de quiniela.

**Respuestas Automáticas**: Utiliza técnicas de web scraping para recopilar automáticamente los resultados de los sorteos de quiniela y proporcionar respuestas precisas a las consultas de los clientes sobre los resultados de los sorteos.

**Gestión de Pedidos**: Los pedidos de boletos de quiniela realizados por los clientes se recopilan en un archivo CSV, que posteriormente se envía a un tablero de control de la agencia de quiniela para su procesamiento por parte del personal.

**Análisis de Ventas**: El chatbot tiene como objetivo principal recopilar información sobre las ventas de los clientes para su posterior análisis. Registra los hábitos de compra de los clientes, lo que permite el desarrollo de estrategias de marketing personalizadas y eficaces.

## Estructura del Repositorio
/src: Contiene el código el codigo de funcion principal "main" y un archivo con las funciones que utiliza el la funcion principal.
/docs: Documentación detallada sobre el funcionamiento del chatbot, incluyendo instrucciones de instalación, configuración y uso.


## Futuros Lineamientos
El proyecto se encuentra en una etapa de desarrollo activo, y en las próximas actualizaciones se introducirán nuevas funcionalidades para mejorar la experiencia del usuario y la eficiencia del chatbot:

**Interpretación Avanzada de Texto**: Se implementará una función de interpretación de texto que utilizará técnicas de minería de texto que analiza un conjunto de mensajes históricos de los clientes. Esto permitirá al chatbot comprender mejor las consultas y ofrecer respuestas más precisas y personalizadas.

**Confirmación de Pagos**: Se integrará la funcionalidad de confirmación de pagos, que permitirá al cliente realizar el pago a través de un link de pago proporcionado por el chatbot y posteriormente verifica el pago por la API de una billetera digital. Esto simplificará el proceso de compra para el cliente y agilizará la gestión de pedidos para la agencia de quiniela.

**Verificación de Boletos con Premio**: Se añadirá una función para verificar si los boletos de quiniela enviados por los clientes tienen premio. Los clientes podrán enviar una foto del ticket de quiniela, y el chatbot utilizará técnicas de procesamiento de imágenes, como Tesseract OCR, para analizar la imagen y determinar si el boleto tiene premio o no.
