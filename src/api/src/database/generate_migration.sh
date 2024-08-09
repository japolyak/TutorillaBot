echo 'Enter migration name'
read -p '' name

cd ..

echo
alembic revision --autogenerate -m "$name"