from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import psutil
import platform
from datetime import datetime

@register("n-tool", "Liangxiu", "多功能工具插件", "1.1.0")
class NToolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("menu")
    async def show_menu(self, event: AstrMessageEvent):
        '''功能菜单'''
        menu_content = """
NTool 功能菜单
1. 状态 → /status
2. 帮助 → /help
3. 信息 → /about
4. 时间 → /time
5. 系统 → /sysinfo
6. 网络 → /netstat
        """
        yield event.plain_result(menu_content.strip())

    @filter.command("status")
    async def show_status(self, event: AstrMessageEvent):
        '''系统状态'''
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%m-%d %H:%M")
        
        status_message = f"""
系统状态
CPU: {cpu_percent}% | 内存: {mem.percent}%
磁盘: {disk.percent}% | 已运行: {boot_time}
        """
        yield event.plain_result(status_message.strip())

    @filter.command("time")
    async def show_time(self, event: AstrMessageEvent):
        '''当前时间'''
        now = datetime.now()
        time_message = f"""
时间信息
{now.strftime("%Y-%m-%d %H:%M:%S")}
星期{["一","二","三","四","五","六","日"][now.weekday()]}
        """
        yield event.plain_result(time_message.strip())

    @filter.command("sysinfo")
    async def system_info(self, event: AstrMessageEvent):
        '''系统信息'''
        sys_info = f"""
系统信息
{platform.system()} {platform.release()}
架构: {platform.machine()} | Python: {platform.python_version()}
        """
        yield event.plain_result(sys_info.strip())

    @filter.command("netstat")
    async def network_status(self, event: AstrMessageEvent):
        '''网络状态'''
        net_io = psutil.net_io_counters()
        net_message = f"""
网络状态
↑{net_io.bytes_sent/1024/1024:.1f}MB
↓{net_io.bytes_recv/1024/1024:.1f}MB
        """
        yield event.plain_result(net_message.strip())

    @filter.command("help")
    async def show_help(self, event: AstrMessageEvent):
        '''帮助'''
        help_message = """
命令列表
/menu    - 功能菜单
/status  - 系统状态
/time    - 当前时间
/sysinfo - 系统信息
/netstat - 网络状态
/help    - 帮助信息
        """
        yield event.plain_result(help_message.strip())

    @filter.command("about")
    async def about_plugin(self, event: AstrMessageEvent):
        '''插件信息'''
        about_message = """
N-Tool v1.1
作者: Liangxiu
功能: 系统监控/信息查询
        """
        yield event.plain_result(about_message.strip())

    async def terminate(self):
        logger.info("N-Tool 插件卸载")
