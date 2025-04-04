from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import psutil
import platform
from datetime import datetime

@register("n-tool", "Liangxiu", "Multi-functional Utility Plugin", "1.3.1")
class NToolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("menu")
    async def show_menu(self, event: AstrMessageEvent) -> MessageEventResult:
        """Show command menu"""
        return event.plain_result("""
[COMMAND MENU]
----------------
/status  - System metrics
/time    - Current time
/sysinfo - System specs
/netstat - Network stats
/help    - Command help
----------------
""".strip())

    @filter.command("status")
    async def show_status(self, event: AstrMessageEvent) -> MessageEventResult:
        """Show system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return event.plain_result(f"""
[SYSTEM STATUS]
----------------
CPU: {cpu_percent}% (1m avg)
RAM: {mem.percent}% ({mem.used//(1024**2)}/{mem.total//(1024**2)} MiB)
DISK: {disk.percent}% ({disk.used//(1024**3)}/{disk.total//(1024**3)} GiB)
UPTIME: {str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))[:-7]}
----------------
""".strip())

    @filter.command("time")
    async def show_time(self, event: AstrMessageEvent) -> MessageEventResult:
        """Show timestamp"""
        now = datetime.now()
        return event.plain_result(f"""
[TIME]
----------------
UTC{now.strftime("%z")} {now.strftime("%Y-%m-%d %H:%M:%S")}
Weekday: {now.strftime("%a").upper()}
Timestamp: {int(now.timestamp())}
----------------
""".strip())

    @filter.command("sysinfo")
    async def system_info(self, event: AstrMessageEvent) -> MessageEventResult:
        """Show hardware info"""
        return event.plain_result(f"""
[SYSTEM INFO]
----------------
OS: {platform.system()} {platform.release()}
Arch: {platform.machine().upper()}
Kernel: {platform.version().split()[0]}
Py: {platform.python_version()}
CPU: {platform.processor().split('@')[0].strip()}
----------------
""".strip())

    @filter.command("netstat")
    async def network_status(self, event: AstrMessageEvent) -> MessageEventResult:
        """Show network I/O"""
        net_io = psutil.net_io_counters()
        return event.plain_result(f"""
[NETWORK]
----------------
TX: {net_io.bytes_sent//(1024**2)} MiB
RX: {net_io.bytes_recv//(1024**2)} MiB
Pkts: TX{net_io.packets_sent}/RX{net_io.packets_recv}
ERR: TX{net_io.errout}/RX{net_io.errin}
----------------
""".strip())

    @filter.command("help")
    async def show_help(self, event: AstrMessageEvent) -> MessageEventResult:
        """Show command reference"""
        return event.plain_result("""
[HELP]
----------------
/status  - Live system metrics
/time    - Timestamp & timezone
/sysinfo - Hardware specifications
/netstat - Network throughput
/help    - This message
/menu    - Command list
----------------
""".strip())

    async def terminate(self):
        logger.info("N-Tool plugin terminated")
