/**
 * Actualizar package.json con scripts de testing
 * 
 * Agregar estos scripts a la sección "scripts" de package.json:
 * 
 * {
 *   "scripts": {
 *     "dev": "vite",
 *     "build": "tsc && vite build",
 *     "preview": "vite preview",
 *     "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
 *     "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
 *     "test": "jest",
 *     "test:watch": "jest --watch",
 *     "test:coverage": "jest --coverage",
 *     "test:ui": "jest --coverage --collectCoverageFrom='src/**/*.{ts,tsx}'",
 *     "type-check": "tsc --noEmit"
 *   }
 * }
 * 
 * Dependencias de desarrollo necesarias (ya debería estar en package.json):
 * 
 * {
 *   "devDependencies": {
 *     "@testing-library/jest-dom": "^6.1.5",
 *     "@testing-library/react": "^14.1.2",
 *     "@testing-library/user-event": "^14.5.1",
 *     "@types/jest": "^29.5.11",
 *     "jest": "^29.7.0",
 *     "jest-environment-jsdom": "^29.7.0",
 *     "ts-jest": "^29.1.1",
 *     "identity-obj-proxy": "^3.0.0"
 *   }
 * }
 */

export const TESTING_SETUP = `
# Testing Setup Instructions

## 1. Instalar Dependencias

\`\`\`bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest ts-jest @types/jest jest-environment-jsdom identity-obj-proxy
\`\`\`

## 2. Archivos de Configuración

✅ jest.config.js - Configuración principal
✅ jest.setup.ts - Setup global

## 3. Scripts Disponibles

\`\`\`bash
npm test                # Ejecutar tests
npm run test:watch     # Modo watch
npm run test:coverage  # Reporte de cobertura
npm run test:ui        # UI de cobertura
\`\`\`

## 4. Estructura de Tests

\`\`\`
src/
├── components/
│   ├── tasks/
│   │   ├── TaskCard.tsx
│   │   ├── TaskForm.tsx
│   │   └── __tests__/
│   │       ├── TaskCard.test.tsx
│   │       └── TaskForm.test.tsx
│   └── projects/
│       ├── ProjectCard.tsx
│       ├── __tests__/
│       └── ProjectCard.test.tsx
├── pages/
│   ├── TasksPage.tsx
│   ├── ProjectsPage.tsx
│   └── __tests__/
│       ├── TasksPage.test.tsx
│       └── ProjectsPage.test.tsx
└── hooks/
    ├── useTask.ts
    ├── useAuth.ts
    └── __tests__/
        ├── useTask.test.ts
        └── useAuth.test.ts
\`\`\`

## 5. Coverage Targets

- Branches: 70%
- Functions: 70%
- Lines: 70%
- Statements: 70%

## 6. Comando para Coverage Completo

\`\`\`bash
npm run test:coverage
\`\`\`

Esto generará:
- Terminal output con percentages
- Carpeta \`coverage/\` con reportes HTML
`;
