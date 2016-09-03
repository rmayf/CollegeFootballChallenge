export PYTHONPATH="$PYTHONPATH:$HOME/CollegeFootballChallenge/django"
export DJANGO_SETTINGS_MODULE="cfbc.settings"
ITTHICRON_DIR="${HOME}/CollegeFootballChallenge/django/Itthicron"
export PATH="$PATH:/usr/local/bin:${ITTHICRON_DIR}"

if [ $1 ]; then
   #cmd line param is the Itthicron script to run
   cd ${ITTHICRON_DIR}
   ./$1
fi
