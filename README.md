# COE418 Final Project

## Overview
This is the final project for COE418. The project uses Docker for containerization and includes a Makefile for easy project management.

## Project Structure
```
.
├── Makefile                 # Build and project management commands
├── docker-compose.yml       # Docker composition for containerized services
├── srcs/                    # Source code directory
└── .gitignore              # Git ignore file
```

## Prerequisites
- Docker
- Docker Compose
- Make

## Getting Started

### Build and Run
Use the Makefile to manage the project:

```bash
make help          # View available commands
make build         # Build the project
make up            # Start services
make down          # Stop services
```

Or use Docker Compose directly:

```bash
docker-compose up -d      # Start services in background
docker-compose down       # Stop services
docker-compose logs       # View service logs
```

## Development

The project is organized with source files in the `srcs/` directory. Modify files as needed and rebuild using the commands above.

## Authors
Omar Dana (ApparentlyVenus), Kasem Smaily
