#once scripts are copied to correct directories
service nginx restart
supervisorctl reread
supervisorctl update
supervisorctl update GoldDigger