# BattleHub - Tournament Platform

##  Quick Start

```bash
venv\Scripts\activate
python manage.py runserver
```

##  Docker Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Rebuild and start (after code changes)
docker compose up -d --build

# View logs
docker compose logs -f web
docker compose logs -f nginx
docker compose logs -f db

# Restart specific service
docker compose restart web
docker compose restart nginx
```

##  Database (PostgreSQL) Commands

```bash
# Enter PostgreSQL interactive mode
docker compose exec -it db psql -U battlehub_user -d battlehub

# View all tables
docker compose exec -e PAGER=cat db psql -U battlehub_user -d battlehub -c '\dt'

# View all users
docker compose exec -e PAGER=cat db psql -U battlehub_user -d battlehub -c 'SELECT id, username, email FROM auth_user;'

# View all tournaments
docker compose exec -e PAGER=cat db psql -U battlehub_user -d battlehub -c 'SELECT id, name, status FROM tournaments_tournament;'

# View matches
docker compose exec -e PAGER=cat db psql -U battlehub_user -d battlehub -c 'SELECT id, tournament_id, round_number, is_finished FROM tournaments_match;'

# View votes
docker compose exec -e PAGER=cat db psql -U battlehub_user -d battlehub -c 'SELECT * FROM tournaments_matchvote;'

# View table structure
docker compose exec -e PAGER=cat db psql -U battlehub_user -d battlehub -c '\d tournaments_tournament'
```

##  Django Management Commands

```bash
# Run inside Docker container
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic
docker compose exec web python manage.py shell

# Or locally with venv
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

##  Ngrok (External Access)

```bash
grok http 8000
# or
ngrok http 80   # for Docker/nginx
```

##  Important Files

- `battlehub/settings.py` - Django settings
- `docker-compose.yml` - Docker services config
- `nginx.conf` - Nginx configuration
- `.env` - Environment variables

##  Database Credentials

```
Database: battlehub
User: battlehub_user
Password: battlehub_pass
Host: db (Docker) / localhost (local)
Port: 5432
```