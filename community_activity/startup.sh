echo $HOME
date

echo $EWALLET > ewallet.pem
echo $TNS_NAMES > tnsnames.ora
cat tnsnames.ora
gunicorn main:app --bind :$PORT --workers 4 --threads 8 --timeout 0 --worker-class uvicorn.workers.UvicornWorker