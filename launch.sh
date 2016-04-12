git add -A;
git commit -m "$1";
git push heroku master
heroku ps:scale web=1

