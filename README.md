# OrangeMilk-Bot-Next

基于 NoneBot2 实现的 Bot 库

## 一、如何开始

### 1. 克隆本仓库
使用 `git clone` 拉取代码

### 2. 安装 NoneBot2 CLI 工具
参考 [NoneBot2 官网](https://nonebot.dev/) 文档安装 `pipx`、`nb-cli` 等必要的工具

### 3. 安装虚拟环境
> 推荐使用 `virtualenv` 而不是 `conda` 等，原因是：
> - 此项目单独占用的环境，不必再其他地方发现（例如它不必被展示在 `conda env list` 中
> - `nb-cli` 工具对 `virtualenv` 适配较好

安装 `virtualenv`：
```bash
pip install virtualenv
```

**先进入本项目目录**，然后创建虚拟环境，**推荐命名为 `.venv`**，因为 `nb-cli` 默认以 `.venv` 作为虚拟环境目录
```bash
virtualenv .venv
```

使能环境
```bash
# Linux 环境
source ./.venv/bin/activate

# Windows Powershell
./.venv/Scripts/activate

# Windows CMD (命令提示符)
.venv\Scripts\activate
```

### 4. 填写配置文件

####  1、`.env.prod`

```toml
DRIVER=~fastapi
PORT=1281

# 填写机器人主人的QQ号
# 列表，填入的 QQ 号会用作 Debug 插件的测试号
master_qqs=[1234567890, 1234567891]
```

### 5. 运行项目
使用 `nb run` 运行此项目
