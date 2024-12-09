import yaml

def load_config(file_path):
    """
    从 YAML 文件中加载配置。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"配置文件 {file_path} 未找到。")
    except yaml.YAMLError as e:
        print(f"加载配置文件时出错: {e}")
    return None