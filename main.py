from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import psutil  # 用于获取系统状态

@register("n-tool", "YourName", "多功能工具插件", "1.0.0")
class NToolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("menu")
    async def show_menu(self, event: AstrMessageEvent):
        '''显示功能菜单'''
        menu_content = """
        === N-Tool 菜单 ===
        1. 系统状态 (/status)
        2. 帮助信息 (/help)
        3. 插件信息 (/about)
        
        请选择功能或直接输入命令
        """
        yield event.plain_result(menu_content)

    @filter.command("status")
    async def show_status(self, event: AstrMessageEvent):
        '''显示系统状态信息'''
        # 获取系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status_message = f"""
        === 系统状态 ===
        CPU 使用率: {cpu_percent}%
        内存使用: {mem.percent}% (已用: {mem.used/1024/1024:.2f}MB / 总计: {mem.total/1024/1024:.2f}MB)
        磁盘使用: {disk.percent}% (已用: {disk.used/1024/1024/1024:.2f}GB / 总计: {disk.total/1024/1024/1024:.2f}GB)
        """
        yield event.plain_result(status_message)

    async def terminate(self):
        '''插件卸载时的清理工作'''
        logger.info("N-Tool 插件正在卸载...")
