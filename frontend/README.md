# AgroBot Frontend

## Project Overview
AgroBot is an AI-powered agricultural assistant frontend built with Webpack and Tailwind CSS.

## Prerequisites
- Node.js (v16 or later)
- npm (v8 or later)

## Setup and Installation

1. Clone the repository
2. Navigate to the frontend directory
```bash
cd frontend
```

3. Install dependencies
```bash
npm install
```

## Development
Run the development server:
```bash
npm start
```
This will start a development server with the following characteristics:
- **Port**: 9000
- **URL**: `http://localhost:9000`
- **Mode**: Development
- **Features**:
  - Hot reloading enabled
  - Open browser automatically
  - Serves files from the `dist` directory

### Additional Development Commands
- `npm run dev`: Build the project in development mode without starting a server
- `npm run build`: Create a production build

## Production Build
Create a production build:
```bash
npm run build
```
The built files will be in the `dist` directory

## Key Technologies
- Webpack 5
- Tailwind CSS
- jQuery
- LocalStorage for chat history management

## Features
- Responsive design
- Persistent chat history
- Collapsible bot information section
- Real-time chat with backend API

## Configuration
- `webpack.config.js`: Webpack configuration
- `tailwind.config.js`: Tailwind CSS customization
- `postcss.config.js`: PostCSS configuration

## Environment
Ensure your backend API is running at `http://127.0.0.1:5000/chat` 