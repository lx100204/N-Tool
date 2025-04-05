from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import psutil
import platform
from datetime import datetime
import subprocess  # 导入 subprocess 模块以执行系统命令
import asyncio  # 导入 asyncio 模块

@register("n-tool", "Liangxiu", "多功能工具插件", "1.2.0")
class NToolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        logger.info("N-Tool 插件已加载")  # 添加插件加载时的日志信息

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
7. Ping  → /ping <host>
        """
        yield event.plain_result(menu_content.strip())

    @filter.command("status")
    async def show_status(self, event: AstrMessageEvent):
        '''系统状态'''
        cpu_percent = psutil.cpu_percent(interval=1)  # 获取 CPU 使用率
        mem = psutil.virtual_memory()  # 获取内存信息
        disk = psutil.disk_usage('/')  # 获取根目录磁盘使用情况
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%m-%d %H:%M")  # 获取系统启动时间并格式化

        status_message = f"""
系统状态
CPU: {cpu_percent}% | 内存: {mem.percent}% ({mem.used/1024/1024:.1f}MB/{mem.total/1024/1024:.1f}MB)
磁盘: {disk.percent}% ({disk.used/1024/1024:.1f}MB/{disk.total/1024/1024:.1f}MB) | 已运行: {boot_time}
        """
        yield event.plain_result(status_message.strip())

    @filter.command("time")
    async def show_time(self, event: AstrMessageEvent):
        '''当前时间'''
        now = datetime.now()  # 获取当前时间
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
        net_io = psutil.net_io_counters()  # 获取网络 I/O 计数器
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
/ping <host> - 检测网络连通性
/help    - 帮助信息
        """
        yield event.plain_result(help_message.strip())

    @filter.command("about")
    async def about_plugin(self, event: AstrMessageEvent):
        '''插件信息'''
        about_message = f"""
N-Tool v1.2
作者: Liangxiu
功能: 系统监控/信息查询/网络检测
        """
        yield event.plain_result(about_message.strip())

    @filter.command("ping")
    async def ping_host(self, event: AstrMessageEvent, host: str):
        '''检测网络连通性'''
        try:
            # 根据操作系统构建 ping 命令
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '3', host]  # Windows 下 ping 3 次，其他系统 ping 3 次

            # 使用 asyncio 创建异步子进程
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                ping_result = stdout.decode('gbk' if platform.system().lower() == 'windows' else 'utf-8') # 根据系统编码解码
                yield event.plain_result(f"Ping {host} 成功:\n{ping_result}")
            else:
                error_result = stderr.decode('gbk' if platform.system().lower() == 'windows' else 'utf-8')
                yield event.plain_result(f"Ping {host} 失败:\n{error_result}")
        except FileNotFoundError:
            yield event.plain_result("错误: 'ping' 命令未找到，请检查系统环境。")
        except Exception as e:
            logger.error(f"执行 ping 命令时发生错误: {e}")
            yield event.plain_result(f"执行 ping 命令时发生未知错误: {e}")

    async def terminate(self):
        logger.info("N-Tool 插件卸载")
