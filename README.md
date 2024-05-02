# Aiogram template



### Project launch. 
command-line flag `--build` optional
``` 
docker-compose -f docker-compose.yml up --build
``` 

### Working with migrations 
Auto-generation after model changes "migration name", 
meaningful name
``` 
docker-compose -f docker-compose.yml exec bot alembic revision --autogenerate -m "migration name"
``` 

Apply all migrations
``` 
docker-compose -f docker-compose.yml exec bot alembic upgrade head
```

Rollback to 1 migration
``` 
docker-compose -f docker-compose.yml exec bot alembic downgrade -1
``` 

