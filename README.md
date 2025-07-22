# LangChain 智能研究助手 - UV 极速部署指南

本指南将引导您使用最新、最快的 Python 包管理工具 `uv` 来部署和运行一个 LangChain 智能体。`uv` 会为项目创建一个纯净、隔离的运行环境，避免污染您的系统全局环境。

### ✨ 升级亮点 (为什么使用 UV？)

*   **极速安装**: 比传统的 `pip` 快 10-100 倍，秒速完成环境配置。
*   **纯净的环境**: `uv` 会为本项目创建一个专属的、隔离的“工作间” (`.venv` 文件夹)，所有依赖都安装在这里，绝不会影响您电脑上其他的 Python 项目。
*   **一体化工具**: 一个 `uv` 命令 = `python -m venv` + `pip`，操作更简洁。

---

## 准备工作

在开始之前，你需要：
1.  **安装 Python**: 确保你的电脑上安装了 Python 3.8 或更高版本。可以从 [Python 官网](https://www.python.org/downloads/) 下载。
2.  **获取 API Keys**: 本程序需要两个 API Key，请先注册并获取：
    *   **SiliconFlow API Key**: 用于驱动大语言模型“大脑”。
        *   注册地址: [https://platform.siliconflow.cn/](https://platform.siliconflow.cn/)
        *   登录后在“API 密钥”页面创建。
    *   **Tavily API Key**: 用于提供实时搜索“能力”。
        *   注册地址: [https://app.tavily.com/](https://app.tavily.com/)
        *   注册后在 Dashboard 页面就能看到你的 Key。

---

## 部署步骤

### 步骤零：安装 UV

您需要先在您的电脑上安装 `uv`。打开终端或命令提示符，根据您的操作系统选择对应的命令执行即可。

**Windows (使用 PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux (使用 a Shell):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
安装完成后，关闭并重新打开终端，以确保 `uv` 命令生效。更多安装方式请参考 [UV 官方文档](https://github.com/astral-sh/uv#installation)。

### 步骤一：下载项目文件

确保您的项目文件夹中包含 `main.py`, `requirements.txt`, 和 `.env.example` 文件。

### 步骤二：配置 API Keys

1.  在项目文件夹中，找到 `.env.example` 文件。
2.  **复制并重命名**该文件为 `.env`。
3.  用文本编辑器打开新的 `.env` 文件，将您获取的 API Keys 填入，并保存。

    **修改后 (示例):**
    ```
    SILICONFLOW_API_KEY='sf_xxxxxxxxxxxxxxxxxx'
    TAVILY_API_KEY='tvly-yyyyyyyyyyyyyyyyy'
    ```

### 步骤三：创建环境并安装依赖 (核心步骤)

1.  **打开终端**，并使用 `cd` 命令进入您的项目文件夹。
    ```bash
    # 示例
    cd path/to/your/langchain_agent_project
    ```
2.  **创建虚拟环境**: 运行以下命令，`uv` 会在当前目录下创建一个名为 `.venv` 的文件夹，这就是我们隔离的“工作间”。
    ```bash
    uv venv
    ```
3.  **激活环境**: 必须先“进入”这个工作间，后续操作才会在其中进行。
    *   **Windows (CMD):**
        ```cmd
        .venv\Scripts\activate
        ```
    *   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
    *   **macOS / Linux:**
        ```bash
        source .venv/bin/activate
        ```
    成功激活后，您会看到终端提示符前面出现了 `(.venv)` 的字样。

4.  **安装依赖**: 在已激活的环境中，使用 `uv` 安装所有必需的库。
    ```bash
    uv pip install -r requirements.txt
    ```
    您将体验到飞一般的安装速度！

### 步骤四：运行程序！

确保您的虚拟环境仍处于**激活状态**（终端提示符前有 `(.venv)`），运行程序：

```bash
python main.py
```

程序启动，智能体初始化完成后，您就可以开始提问了！

---

### 日常使用 (再次运行时)

当您关闭终端后想再次运行此程序，无需重复所有步骤。只需：

1.  打开终端，`cd` 到项目文件夹。
2.  **激活环境** (参考步骤三的第 3 点)。
3.  运行 `python main.py`。

---

### 常见问题 (FAQ)

*   **问：运行 `python main.py` 报错 `ModuleNotFoundError: No module named 'langchain'`？**
    *   **答：** 您很可能忘记激活虚拟环境了！请检查终端提示符前是否有 `(.venv)` 标志。如果没有，请执行步骤三中的第 3 点来激活环境，然后再运行程序。

---
**恭喜！您已经学会了使用现代化工具 `uv` 来部署和管理您的 AI 应用！**