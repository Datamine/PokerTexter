# for destroying heroku apps
for app in $(heroku apps); do heroku apps:destroy --app $app --confirm $app; done
