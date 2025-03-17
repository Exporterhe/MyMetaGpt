import subprocess
from metagpt.logs import logger
class SimpleRunCode:
    name: str="SimpleRunCode"

    async def run(self,code_text: str):
        result = subprocess.run(["python","-c",code_text],capture_output=True,text=True)


        code_result = result.stdout
        logger.info(f"code_result: {code_result}")
        return code_result

