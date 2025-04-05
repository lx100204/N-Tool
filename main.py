from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import psutil
import platform
from datetime import datetime
import subprocess
import re

@register("n-tool", "Liangxiu", "Multi-functional Utility Plugin", "1.3.3")
class NToolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self._cpu_info = self._get_cpu_info()

    def _get_cpu_info(self) -> str:
        """Cross-platform CPU info fetcher"""
        try:
            if platform.system() == "Windows":
                return platform.processor()
            elif platform.system() == "Darwin":
                return subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()
            elif platform.system() == "Linux":
                with open('/proc/cpuinfo') as f:
                    for line in f:
                        if 'model name' in line:
                            return re.sub('.*model name.*:', '', line, 1).strip()
                return "Unknown CPU"
            return platform.processor()[:32]
        except Exception as e:
            logger.warning(f"CPU info fetch failed: {str(e)}")
            return "Unknown CPU"

    @filter.command("menu")
    async def show_menu(self, event: AstrMessageEvent, *args, **kwargs):
        """Show command menu"""
        return event.reply("""
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
    async def show_status(self, event: AstrMessageEvent, *args, **kwargs):
        """Show system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return event.reply(f"""
[SYSTEM STATUS]
----------------
CPU: {cpu_percent}% (1m avg)
RAM: {mem.percent}% ({mem.used//(1024**2)}/{mem.total//(1024**2)} MiB)
DISK: {disk.percent}% ({disk.used//(1024**3)}/{disk.total//(1024**3)} GiB)
UPTIME: {str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))[:-7]}
----------------
""".strip())

    @filter.command("time")
    async def show_time(self, event: AstrMessageEvent, *args, **kwargs):
        """Show timestamp"""
        now = datetime.now()
        return event.reply(f"""
[TIME]
----------------
UTC{now.strftime("%z")} {now.strftime("%Y-%m-%d %H:%M:%S")}
Weekday: {now.strftime("%a").upper()}
Timestamp: {int(now.timestamp())}
----------------
""".strip())

    @filter.command("sysinfo")
    async def system_info(self, event: AstrMessageEvent, *args, **kwargs):
        """Show hardware info"""
        return event.reply(f"""
[SYSTEM INFO]
----------------
OS: {platform.system()} {platform.release()}
Arch: {platform.machine().upper()}
Kernel: {platform.version().split()[0]}
Py: {platform.python_version()}
CPU: {self._cpu_info}
Cores: {psutil.cpu_count(logical=False)}P/{psutil.cpu_count()}T
----------------
""".strip())

    @filter.command("netstat")
    async def network_status(self, event: AstrMessageEvent, *args, **kwargs):
        """Show network I/O"""
        net_io = psutil.net_io_counters()
        return event.reply(f"""
[NETWORK]
----------------
TX: {net_io.bytes_sent//(1024**2)} MiB
RX: {net_io.bytes_recv//(1024**2)} MiB
Pkts: TX{net_io.packets_sent}/RX{net_io.packets_recv}
ERR: TX{net_io.errout}/RX{net_io.errin}
----------------
""".strip())

    @filter.command("help")
    async def show_help(self, event: AstrMessageEvent, *args, **kwargs):
        """Show command reference"""
        return event.reply("""
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
