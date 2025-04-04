from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import psutil
import platform
from datetime import datetime

@register("n-tool", "Liangxiu", "Multi-functional Utility Plugin", "1.3.0")
class NToolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("menu")
    async def show_menu(self, event: AstrMessageEvent):
        """Show command menu"""
        menu_content = """
[COMMAND MENU]
----------------
1. /status  - System metrics
2. /time    - Current time
3. /sysinfo - System specs
4. /netstat - Network stats
5. /help    - Command help
----------------
        """
        yield event.plain_result(menu_content.strip())

    @filter.command("status")
    async def show_status(self, event: AstrMessageEvent):
        """Show system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status_message = f"""
[SYSTEM STATUS]
----------------
CPU: {cpu_percent}% (1m avg)
RAM: {mem.percent}% ({mem.used//(1024**2)}/{mem.total//(1024**2)} MiB)
DISK: {disk.percent}% ({disk.used//(1024**3)}/{disk.total//(1024**3)} GiB)
UPTIME: {str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))[:-7]}
----------------
        """
        yield event.plain_result(status_message.strip())

    @filter.command("time")
    async def show_time(self, event: AstrMessageEvent):
        """Show timestamp"""
        now = datetime.now()
        time_message = f"""
[TIME]
----------------
UTC{now.strftime("%z")} {now.strftime("%Y-%m-%d %H:%M:%S")}
Weekday: {now.strftime("%a").upper()}
Timestamp: {int(now.timestamp())}
----------------
        """
        yield event.plain_result(time_message.strip())

    @filter.command("sysinfo")
    async def system_info(self, event: AstrMessageEvent):
        """Show hardware info"""
        sys_info = f"""
[SYSTEM INFO]
----------------
OS: {platform.system()} {platform.release()}
Arch: {platform.machine().upper()}
Kernel: {platform.version().split()[0]}
Py: {platform.python_version()}
CPU: {platform.processor().split('@')[0].strip()}
----------------
        """
        yield event.plain_result(sys_info.strip())

    @filter.command("netstat")
    async def network_status(self, event: AstrMessageEvent):
        """Show network I/O"""
        net_io = psutil.net_io_counters()
        net_message = f"""
[NETWORK]
----------------
TX: {net_io.bytes_sent//(1024**2)} MiB
RX: {net_io.bytes_recv//(1024**2)} MiB
Pkts: TX{net_io.packets_sent}/RX{net_io.packets_recv}
ERR: TX{net_io.errout}/RX{net_io.errin}
----------------
        """
        yield event.plain_result(net_message.strip())

    @filter.command("help")
    async def show_help(self, event: AstrMessageEvent):
        """Show command reference"""
        help_message = """
[HELP]
----------------
/status  - Live system metrics
/time    - Timestamp & timezone
/sysinfo - Hardware specifications
/netstat - Network throughput
/help    - This message
/menu    - Command list
----------------
        """
        yield event.plain_result(help_message.strip())

    async def terminate(self):
        logger.info("N-Tool plugin terminated")
