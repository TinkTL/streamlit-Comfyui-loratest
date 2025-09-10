import copy
import json
import os
import random


DEFAULT_WORKFLOW_PATH = f"workflows/Free_Creativity_api.json"
host = "http://10.99.0.19:30060"

prompt_url = f"{host}/prompt"

with open(DEFAULT_WORKFLOW_PATH, 'r', encoding='utf-8') as f:
    workflow_source_data = json.load(f)


def Free_Creativity(
        prompt: str = None,
        # workflow_path: str = DEFAULT_WORKFLOW_PATH,
) -> str:
    workflow_data = copy.deepcopy(workflow_source_data)
    try:
        # 检查并修改提示词节点
        if "10001" not in workflow_data:
            return f"error: 工作流中缺少必要的节点10001(随机种子)"
        random_seed = random.randint(1, 9999999999999999)
        workflow_data["10001"]["inputs"]["noise_seed"] = random_seed

        if "10000" not in workflow_data:
            return f"error: 工作流中缺少必要的节点10000(提示词输入)"
        if prompt:
            workflow_data["10000"]["inputs"]["string"] = prompt
    except Exception as e:
        print(f"修改工作流出错: {str(e)}")
        return f"修改工作流出错: {str(e)}"
    print("Free_Creativity")

    from utils.getImage import send_prompt
    return send_prompt(workflow_data, host, node_id="20002")