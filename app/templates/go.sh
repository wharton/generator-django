psql postgres -c "CREATE USER django_user WITH PASSWORD '1qaz2wsx'"
psql -d <%= _.slugify(databaseName) %> -tc "SELECT 1 FROM pg_database WHERE datname = '<%= _.slugify(databaseName) %>'"| grep -q 1 || psql postgres -c "CREATE DATABASE <%= _.slugify(databaseName) %> WITH OWNER django_user"

echo  "User django_user created or exists. This is good."
echo  "User django_user is now an owner of <%= _.slugify(databaseName) %> database."
