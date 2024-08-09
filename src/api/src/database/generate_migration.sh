echo 'Enter migration name'
read -p '' migvar

cd ..

echo
echo "This is your migration name - $migvar"

echo
alembic revision --autogenerate -m "$migvar"