from daemon_scheduler import DaemonScheduler

scheduler = DaemonScheduler(interval=10)  # log every 10 seconds
scheduler.run()