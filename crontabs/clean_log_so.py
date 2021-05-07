

#Aun no se porque se acumula mucho log, esto elimina diario, averiguar el fondo

# Script que crea crontab que permite limpiar logs que se genera en el S.O

# result: 0 0 * * * rm -rf /var/log/log/*.log
from crontab import CronTab
cron = CronTab(user='yachaycode')

job = cron.new(command='rm -rf /var/log/log/*.log', comment='clear_log_var')
job.minute.also.on(0)
job.hour.also.on(0)
cron.write()


job = cron.new(command='echo ""> /var/log/syslog', comment='clear_log_var_syslog')
job.minute.also.on(0)
job.hour.also.on(5)
cron.write()

job = cron.new(command='echo ""> /var/log/syslog.1', comment='clear_log_var_syslog1')
job.minute.also.on(0)
job.hour.also.on(5)
cron.write()

# result all cron

# 0 0 * * * rm -rf /var/log/log/*.log
# 0 5 * * * echo ""> /var/log/syslog
# 0 5 * * * echo ""> /var/log/syslog.1

