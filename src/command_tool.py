import shlex  # 导入shlex库，用于正确解析命令行输入
from config import Config  # 从config模块导入Config类，用于配置管理
from github_client import GitHubClient  # 从github_client模块导入GitHubClient类，用于GitHub API操作
from hackernews_client import HackerNewsClient  # 从hackernews_client模块导入HackerNewsClient类，用于HackerNews API操作
from report_generator import ReportGenerator  # 从report_generator模块导入ReportGenerator类，用于报告生成
from llm import LLM  # 从llm模块导入LLM类，可能用于语言模型相关操作
from subscription_manager import SubscriptionManager  # 从subscription_manager模块导入SubscriptionManager类，管理订阅
from command_handler import CommandHandler  # 从command_handler模块导入CommandHandler类，处理命令行命令
from logger import LOG  # 从logger模块导入LOG对象，用于日志记录

def main():
    config = Config()  # 创建配置实例
    github_client = GitHubClient(config.github_token)  # 创建GitHub客户端实例
    hackernews_client = HackerNewsClient()  # 创建HackerNews客户端实例
    llm = LLM()  # 创建语言模型实例
    report_generator = ReportGenerator(llm)  # 创建报告生成器实例
    subscription_manager = SubscriptionManager(config.subscriptions_file)  # 创建订阅管理器实例
    command_handler = CommandHandler(github_client, subscription_manager, hackernews_client, report_generator)  # 创建命令处理器实例

    github_parser = command_handler.github_parser  # 获取GitHub命令解析器
    hackernews_parser = command_handler.hackernews_parser  # 获取HackerNews命令解析器

    while True:
        try:
            command_handler.print_source_help()
            source = input("Source> ")  # 等待用户输入
            if source in ['exit', 'quit']:  # 如果输入为退出命令，则结束循环
                break
            parser = None
            if source == 'github':  # 如果用户输入的命令为GitHub
                parser = github_parser
            elif source == 'hackernews':  # 如果用户输入的命令为HackerNews
                parser = hackernews_parser
            parser.print_help()  # 打印命令帮助信息
            while True:
                user_input = input("Action> ")  # 等待用户输入
                if user_input in ['back', 'up']:  # 如果输入为退出命令，则结束循环
                    break
                try:
                    args = parser.parse_args(shlex.split(user_input))  # 解析用户输入的命令
                    if args.command is None:  # 如果没有命令被解析，则继续循环
                        continue
                    args.func(args)  # 执行对应的命令函数
                except SystemExit as e:  # 捕获由于错误命令引发的异常
                    LOG.error("Invalid command. Type 'help' to see the list of available commands.")                    
        except Exception as e:
            LOG.error(f"Unexpected error: {e}")  # 记录其他未预期的错误

if __name__ == '__main__':
    main()  # 如果直接运行该文件，则执行main函数
