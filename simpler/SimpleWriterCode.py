import re
import asyncio
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger

# 继承action
class SimpleWriteCode(Action):
    PROMPT_TEMPLATE: str= """
    Write a python function that can {instruction} and provide two runnnable test cases.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """
    name: str="SimpleWriteCode"

# 重写run方法
    async def run(self,instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        # 调用大模型回答
        rsp = await self._aask(prompt)
        code_text = SimpleWriteCode.parse_code(rsp)
        return code_text
    
    @staticmethod
    def parse_code(rsp):
        # 处理回答结果 使用正则式去除多余内容
        pattern = r'```python(.*)```'
        match = re.search(pattern,rsp,re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text

