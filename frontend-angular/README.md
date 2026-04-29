# Frontend — Veu Transcriber

Interfaz web para subir vídeos y obtener su transcripción mediante el backend de lip reading. Construida con Angular 21 y servida en producción con nginx.

## Tecnologías

- **Angular 21** (standalone components, signals)
- **TypeScript**
- **SCSS**
- **nginx** — servidor de producción (en Docker)

## Funcionalidad

1. El usuario selecciona o arrastra un fichero de vídeo.
2. El vídeo se previsualiza en pantalla.
3. Al pulsar *Transcribe*, el fichero se envía al backend (`POST /transcribe`).
4. La transcripción se muestra en pantalla con opción de copiarla.

## Ejecución con Docker (recomendado)

Desde la raíz del monorepo:

```bash
docker compose up --build lipreading-frontend
```

La app quedará disponible en `http://localhost`.

## Desarrollo local

1. Instala las dependencias:

```bash
npm install
```

2. Arranca el servidor de desarrollo:

```bash
ng serve
```

Abre el navegador en `http://localhost:4200`.

> Asegúrate de que el backend está corriendo en `http://localhost:8000` antes de usar la app.

## Build de producción

```bash
ng build --configuration production
```

Los artefactos se generan en `dist/trans-audio/browser/`.

## Tests

```bash
ng test
```

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
