echo $HOME
date

echo $EWALLET | base64 -d > ewallet.pem
echo $TNS_NAMES | base64 -d > tnsnames.ora
cat ewallet.pem
cat tnsnames.ora
gunicorn main:app --bind :$PORT --workers 4 --threads 8 --timeout 0 --worker-class uvicorn.workers.UvicornWorker