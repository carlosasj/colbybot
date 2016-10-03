FROM python:3.5-onbuild

EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]