from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
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
        '''显示功能菜单'''
        menu_content = """
╔═══════════════════════════
║       N-Tool 功能菜单      
╠═══════════════════════════
║ 1. 系统状态   → /status
║ 2. 帮助信息   → /help
║ 3. 插件信息   → /about
║ 4. 时间查询   → /time
║ 5. 系统信息   → /sysinfo
║ 6. 网络状态   → /netstat
║
║ 输入对应命令即可使用功能
╚═══════════════════════════
        """
        yield event.plain_result(menu_content.strip())

    @filter.command("status")
    async def show_status(self, event: AstrMessageEvent):
        '''显示系统状态信息'''
        # 获取系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        
        status_message = f"""
╔═══════════════════════════
║       系统实时状态        
╠═══════════════════════════
║ CPU使用率: {cpu_percent:>6}%
║ 内存使用: {mem.percent:>6}% 
║   ├─ 已用: {mem.used/1024/1024:>8.2f} MB
║   └─ 总计: {mem.total/1024/1024:>8.2f} MB
║
║ 磁盘使用: {disk.percent:>6}%
║   ├─ 已用: {disk.used/1024/1024/1024:>6.2f} GB
║   └─ 总计: {disk.total/1024/1024/1024:>6.2f} GB
║
║ 系统启动时间: {boot_time}
╚═══════════════════════════
        """
        yield event.plain_result(status_message.strip())

    @filter.command("time")
    async def show_time(self, event: AstrMessageEvent):
        '''显示当前时间'''
        now = datetime.now()
        time_message = f"""
╔═══════════════════════════
║       当前时间信息        
╠═══════════════════════════
║ 日期: {now.strftime("%Y年%m月%d日")}
║ 时间: {now.strftime("%H:%M:%S")}
║ 星期: {["一","二","三","四","五","六","日"][now.weekday()]}
║ 时区: UTC{now.strftime("%z")}
╚═══════════════════════════
        """
        yield event.plain_result(time_message.strip())

    @filter.command("sysinfo")
    async def system_info(self, event: AstrMessageEvent):
        '''显示系统基本信息'''
        sys_info = f"""
╔═══════════════════════════
║       系统基本信息        
╠═══════════════════════════
║ 系统: {platform.system()} {platform.release()}
║ 架构: {platform.machine()}
║ 版本: {platform.version()}
║ Python: {platform.python_version()}
║ 处理器: {platform.processor()}
╚═══════════════════════════
        """
        yield event.plain_result(sys_info.strip())

    @filter.command("netstat")
    async def network_status(self, event: AstrMessageEvent):
        '''显示网络状态'''
        net_io = psutil.net_io_counters()
        net_message = f"""
╔═══════════════════════════
║       网络状态信息        
╠═══════════════════════════
║ 发送字节: {net_io.bytes_sent/1024/1024:.2f} MB
║ 接收字节: {net_io.bytes_recv/1024/1024:.2f} MB
║ 发送包数: {net_io.packets_sent}
║ 接收包数: {net_io.packets_recv}
╚═══════════════════════════
        """
        yield event.plain_result(net_message.strip())

    @filter.command("help")
    async def show_help(self, event: AstrMessageEvent):
        '''显示帮助信息'''
        help_message = """
╔═══════════════════════════
║       N-Tool 帮助信息     
╠═══════════════════════════
║ /menu    - 显示功能菜单
║ /status  - 显示系统状态
║ /time    - 显示当前时间
║ /sysinfo - 显示系统信息
║ /netstat - 显示网络状态
║ /help    - 显示本帮助
║ /about   - 插件信息
╚═══════════════════════════
        """
        yield event.plain_result(help_message.strip())

    @filter.command("about")
    async def about_plugin(self, event: AstrMessageEvent):
        '''显示插件信息'''
        about_message = """
╔═══════════════════════════
║      N-Tool 插件信息      
╠═══════════════════════════
║ 名称: N-Tool 多功能工具
║ 版本: 1.1.0
║ 作者: Liangxiu
║ 功能: 系统监控/信息查询
║ 描述: 提供多种实用工具功能
╚═══════════════════════════
        """
        yield event.plain_result(about_message.strip())

    async def terminate(self):
        '''插件卸载时的清理工作'''
        logger.info("N-Tool 插件正在卸载...")
