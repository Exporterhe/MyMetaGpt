import re
import asyncio
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
import SimpleWriterCode,SimpleRunCode

class RunabbleCode(Role):
    name: str="Tom"
    profile: str = "RunnableCoder"

    #初始化所有的action 设置为by_order  按照制定顺序执行action 
    # 覆盖——act 函数 
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.actions = [SimpleWriterCode,SimpleRunCode]
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: 准备 {self.rc.todo}")
        # 通过在底层按顺序选择动作
        # todo 首先是 SimpleWriteCode() 然后是 SimpleRunCode()
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0] # 得到最相似的 k 条消息
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
    
async def main():
    msg = "写一个计算器"
    role = RunabbleCode()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)


if __name__ == "__main__":
    asyncio.run(main())