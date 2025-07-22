# LangGraph 智能研究助理

本项目演示了如何使用 LangGraph 构建一个智能研究助理。该智能体能够搜索网络、评估搜索结果，并决定是否需要优化搜索词或直接生成答案。

## 核心特性

- **循环推理**：如果初始结果不足，智能体可以循环回到搜索步骤优化查询。
- **有状态**：智能体维护着一个包含对话历史和搜索结果的状态。
- **工具使用**：使用 Tavily 进行网络搜索。
- **条件逻辑**：使用 LLM 来决定工作流的下一步。

## 项目结构
```
langgraph-agent-project/
├── .venv/ # uv 管理的虚拟环境
├── src/
│ ├── agent_app/
│ │ ├── agent.py # 核心智能体逻辑
│ │ └── main.py # 项目入口点
├── .env # API 密钥
├── pyproject.toml # 依赖项
└── README.md
```

## 环境设置 (使用 uv)

本项目使用 `uv` 进行高速包管理。

1.  **安装 `uv`：**
    如果您还没安装 `uv`，请遵从官方指引。它是一个单一二进制文件，安装非常简单。
    
    *   **macOS / Linux：**
        ```bash
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ```
    *   **Windows：**
        ```bash
        powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
        ```

2.  **创建并激活虚拟环境：**
    在项目根目录，`uv` 可以为您创建并管理虚拟环境。
    ```bash
    # 使用 Python 3.9+ 创建一个名为 .venv 的虚拟环境
    uv venv
    
    # 激活环境
    source .venv/bin/activate  # 在 Windows 上，使用 `.venv\Scripts\activate`
    ```

3.  **安装依赖项：**
    `uv` 会读取 `pyproject.toml` 文件并以极快的速度安装依赖。
    ```bash
    uv pip install -e .
    ```
    *注意：为了使用 `pygraphviz` 进行图形可视化，您可能需要先在系统层面安装 `graphviz`。*
    *   *macOS:* `brew install graphviz`
    *   *Ubuntu:* `sudo apt-get install graphviz`

4.  **配置 API 密钥：**
    在项目根目录创建一个 `.env` 文件，并填入您的 API 密钥。
    ```bash
    # 您可以用这个命令创建文件结构
    echo 'OPENAI_API_KEY="sk-..."\nTAVILY_API_KEY="tvly-..."' > .env
    
    # 然后，请手动编辑 .env 文件，填入您真实的密钥
    ```

## 如何运行

在项目根目录运行主程序：

```bash
uv run python -m agent_app.main
uv run run-agent
```

或者，在虚拟环境激活的状态下，直接运行：
```
python -m agent_app.main
```

## 开发常用命令 (使用 uv)
- 同步依赖项（根据 pyproject.toml 增删依赖）：
    ```bash
    uv pip sync pyproject.toml
    ```

- 添加一个新的依赖项：
    ```bash
    # 目前 uv 还没有 `add` 命令。
    # 您需要手动编辑 pyproject.toml 文件，然后运行同步命令。
    # 1. 在 pyproject.toml 的 dependencies 列表中添加 "your_package"。
    # 2. 运行: uv pip sync pyproject.toml
    ```
- 不激活虚拟环境直接运行命令
    ```Bash
    uv run <command>
    ```

