import datetime
from cgi_models import Miner
import time
from loguru import logger
from prometheus_client import start_http_server, Summary
import confuse

# Metrics summary
antminer_uptime_seconds = Summary('antminer_uptime_seconds', 'General uptime of miner in seconds')

# you need at least 6 seconds per miner, increase this number if monitoring 16 miners or more
SECONDS_4_CHECKS = 95
    
def is_str_canbe_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        try:
            config = confuse.Configuration('antminer_exporter', __name__)
            config.set_file('antminer_exporter/config.yaml')
            miners = config['miners'].get()
        except confuse.exceptions.ConfigReadError as e:
            logger.error('Can\'t find "config.yaml", is it exists?')
            # logger.exception(e)
            break
        
        miner_list = []

        for miner in miners:  # Create miner objects
            try:
                m = Miner(ip=miner['ip'], cgi_user=miner.get('user', 'root'), cgi_password=miner.get('password', 'root'))
            except KeyError as e:
                if e.args[0] == 'ip':
                    logger.error(f'IP for miner {miner} does not exist')
                elif e.args[0] == 'name':
                    logger.warning(f'Name for miner {miner["ip"]} does not exist')
                else:
                    logger.exception(e)
            if m.is_alive():
                miner_list.append(m)
                if is_str_canbe_int(m.system_info.uptime):
                    uptime = datetime.timedelta(minutes=int(m.system_info.uptime))
                    antminer_uptime_seconds.observe(uptime.total_seconds())
                else:
                    uptime_h, uptime_m = m.system_info.uptime.split(':')
                    uptime = datetime.timedelta(hours=int(uptime_h),minutes=int(uptime_m))
                    antminer_uptime_seconds.observe(uptime.total_seconds())
                # m.verify_kernel_log()
                logger.info(f'Connected! Now monitoring this AntMiner: {m.system_info.hostname or m.system_info.ipaddress}')
            else:
                logger.warning(f'Miner {m.system_info.ipaddress} not working on any pool!')
        seconds_per_miner = abs((SECONDS_4_CHECKS / len(miner_list)) - (4*len(miner_list)))
        logger.info(f'Initialization complete: Found {str(len(miner_list))} AntMiners')
        logger.info('Monitoring ACTIVE. Stop by closing this window or pressing Ctrl+C')
        time.sleep(seconds_per_miner)
