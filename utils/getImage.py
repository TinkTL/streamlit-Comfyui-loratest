import time
import uuid
import requests


def send_prompt(
        workflow_data,
        host: str,
        node_id: str,
) -> str:
    try:
        prompt_url = f"{host}/prompt"
        print(f"发送请求到: {prompt_url}")
        client_id = str(uuid.uuid4())
        # 构建正确的请求格式：包含'prompt'键
        request_data = {
            "prompt": workflow_data,
            "client_id": client_id
        }
        response = requests.post(prompt_url, json=request_data)

        if response.status_code == 200:
            result = response.json()
            prompt_id = result.get('prompt_id')
            if not prompt_id:
                return "error:无法获取任务ID"
            result = get_image(
                prompt_id=str(prompt_id),
                host=host,
                node_id=node_id
            )
            return result
        else:
            return (f"error:请求失败，状态码: {response.status_code}, "
                   f"error:: {response.text}")
    except Exception as e:
        return f"error:发送请求失败: {str(e)}"


def get_image(
        prompt_id: str,
        host: str,
        node_id: str,
        max_retries: int = 60,
        retry_interval: float = 1.0
) -> str:
    for i in range(max_retries):
        response = requests.get(f"{host}/history/{prompt_id}")
        if response.status_code != 200:
            time.sleep(retry_interval)
            continue
        history_data = response.json()
        if prompt_id not in history_data:
            time.sleep(retry_interval)
            continue
        outputs = history_data[prompt_id].get("outputs", {})
        if node_id in outputs:
            urls = outputs[node_id].get('text', [])
        if urls:
            return f"success: {urls}"
    return f"error:获取图片URL出错: {prompt_id} not in history_data"
    print(f"error:获取图片URL出错: {prompt_id} not in history_data")


def send_prompt_and_get_image(
        workflow_data,
        host: str,
        user_id: str,
        workflow_run_id: str,
        node_id: str,
) -> str:
    try:
        prompt_url = f"{host}/prompt"
        print(f"request:发送请求到 {prompt_url}")
        client_id = str(uuid.uuid4())
        # 构建正确的请求格式：包含'prompt'键
        request_data = {
            "prompt": workflow_data,
            "client_id": client_id
        }
        response = requests.post(prompt_url, json=request_data)

        if response.status_code == 200:
            result = response.json()
            prompt_id = result.get('prompt_id')
            if not prompt_id:
                return "error:无法获取任务ID"
            from utils.processing import proc_get_image
            if not proc_get_image(host, user_id, workflow_run_id, prompt_id, client_id):
                return "error:无法获取图片"
            # 直接获取图片URL
            print(f"request:请求地址{host}/history/{prompt_id}")
            from utils.getImage import get_image
            result = get_image(prompt_id=str(prompt_id), host=host, node_id=node_id)
            print(f"success:{result}")
            return result
        else:
            return f"error:请求失败，状态码: {response.status_code}, error:{response.text}"
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        return f"error:发送请求失败: {str(e)}\n{trace}"


if __name__ == "__main__":
    print(get_image("d230f753-1b9d-418a-879b-020b49b0d8ce", "http://10.99.0.19:30050/"))
