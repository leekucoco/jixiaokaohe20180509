#!/bin/sh
PROJDIR=/root/project/jixiaokaohe/
PIDFILE=$PROJDIR/uwsgi.pid
PIDFILECELERY=$PROJDIR/celerypid.pid
cd $PROJDIR

func_kill_ce(){

        if [ -f $PIDFILECELERY ]; then

                kill `cat $PIDFILECELERY`

                rm -f $PIDFILECELERY
                echo -e "successful kill running celery"
        fi
}

func_kill_uwsgi(){

        if [ -f $PIDFILE ]; then
                exec uwsgi --stop $PIDFILE &
                echo -e "successful kill running uwsgi"
        fi
}



if [ "$1" = "stop" ]; then

	echo -e  "Stopping uwsgi............................";
        func_kill_uwsgi
	echo -e  "Stopping celery............................";
	    func_kill_ce

elif [ "$1" = "start" ] ;  then

	echo -e  "Starting uwsgi............................."
    exec uwsgi -i uwsgi.ini &
	echo -e  "starting celery............................."
#	exec nohup gunicorn -w 4  MxShop.wsgi:application -b 0.0.0.0:8080 -p gunicorn.pid --daemon
	exec nohup celery -A Dqrcbankjxkh worker -l info -f logs/celery.log -B --autoscale=10,4  --pidfile celerypid.pid &
	sleep 3s
elif [ "$1" = "restart" ]; then
    echo -e  "ReStarting uwsgi............................."
    func_kill_uwsgi
    sleep 2s
    exec uwsgi -i uwsgi.ini &
    sleep 2s
    func_kill_ce
    sleep 2s
	echo -e  "ReStarting celery............................."
#	exec nohup gunicorn -w 4  MxShop.wsgi:application -b 0.0.0.0:8080 -p gunicorn.pid --daemon
	exec nohup celery -A Dqrcbankjxkh worker -l info -f logs/celery.log -B --autoscale=10,4  --pidfile celerypid.pid &
	sleep 3s
fi
