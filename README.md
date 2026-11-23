# Google Account Security Update Skill

把 Google / Gmail 账号安全信息更新整理成可复用的 Agent Skill：恢复邮箱、恢复电话、Authenticator、两步验证、通行密钥和密码。每个项目都包含提交前的账号核对、保存后的页面回读，以及独立的完成状态。

**入口：[SKILL.md](SKILL.md)** · **语言：简体中文** · **版本：1.0.0**

默认操作顺序：

```text
核对当前账号
  → 恢复邮箱
  → 恢复电话
  → 更换 Authenticator
  → 确认两步验证
  → 创建通行密钥
  → 修改密码
  → 回读、同步私密台账、清理临时资源
```

只执行用户指定项目。顺序是维护经验，具体页面与验证要求以 Google 当前界面为准。

## 安装

这是标准 `SKILL.md` 目录，可交给支持 Agent Skills 的客户端加载。仓库不依赖某个浏览器产品，也不要求安装额外 Python 包。

在项目根目录安装到 `.agents/skills/`（适用于会发现该目录的客户端）：

```bash
mkdir -p .agents/skills
git clone https://github.com/Niutopia/google-account-security-update.git \
  .agents/skills/google-account-security-update
```

Claude Code 项目目录可使用：

```bash
mkdir -p .claude/skills
git clone https://github.com/Niutopia/google-account-security-update.git \
  .claude/skills/google-account-security-update
```

根据客户端选择一个位置即可。需要其他导入方式时，选择包含 `SKILL.md` 的仓库目录；客户端是否自动发现、何时刷新目录，以其实际版本为准。

## 使用示例

```text
使用 google-account-security-update，更新 acct-demo-01 的恢复邮箱、
恢复电话、Authenticator、两步验证、通行密钥和密码。
目标值从我指定的私密凭据引用读取，每完成一项都刷新核对。
如果需要手机或系统原生确认，保留页面让我完成。
结果只使用账号代号，不输出联系方式、密码或种子。
```

也可以只指定一项：

```text
使用 google-account-security-update，只更改 acct-demo-01 的恢复邮箱。
核对新地址是否已验证，并同步私密台账中的当前值和验证状态。
```

[变更请求示例](assets/change-request.example.json) 和 [结果示例](assets/result.example.json) 展示输入、输出结构。它们是说明文件，不是自动化执行器的配置。

## 保留的操作经验

- 多账号窗口在每次敏感提交前核对完整邮箱，避免修改到旧标签页里的另一个账号。
- 恢复邮箱显示在页面上，与邮箱验证完成，是两个不同结果。
- 验证器条目存在、绑定时验证码通过、新登录验证码通过，分别记证据。
- 两步验证总开关单独回读，不由 Authenticator 是否存在推定。
- 通行密钥创建要等系统原生确认完成，再回到 Google 列表核验。
- 密码输入被接受、进入改密表单、改密保存成功和新密码登录成功，分别记录。
- 页面时间保留时区。修改主密码后，邮件客户端的应用专用密码也要单独处理。
- 台账仅更新有证据的目标账号与字段；中断后先回读，再继续。

## 文件

| 文件 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) | Skill 入口、触发条件与逐步流程 |
| [browser-cdp.md](references/browser-cdp.md) | 既有浏览器、可选 AdsPower/CDP、身份核对和资源保护 |
| [verification.md](references/verification.md) | 状态定义、证据要求、台账与收尾 |
| [official-sources.md](references/official-sources.md) | 官方入口、平台行为和适用条件 |
| [change-request.example.json](assets/change-request.example.json) | 只有私密引用占位符的请求示例 |
| [result.example.json](assets/result.example.json) | 部分完成的虚构结果示例 |
| [check_public.py](scripts/check_public.py) | 零依赖公开内容检查器 |

## 脱敏与发布检查

公开内容从操作经验重新编写，只保留通用步骤。真实账号、联系方式、账号环境映射、历史运行文件、截图、Cookie、会话数据、密码和验证器种子均不属于发布内容；运行时私密资料放在运行项目的受保护存储中。

[.gitignore](.gitignore) 使用文件白名单。检查器会检查文件清单、Skill 基础结构、JSON、文档相对链接和常见敏感内容特征，只输出问题类型与位置，不回显命中内容。

```bash
python3 -B scripts/check_public.py
# 明确列出文件后暂存，再检查实际 Git 暂存区：
python3 -B scripts/check_public.py --staged
# 提交后检查所有本地引用可达的提交内容和提交元数据：
python3 -B scripts/check_public.py --history
```

自动检查覆盖常见模式，发布前还需人工查看完整差异；它不是所有敏感信息的穷尽证明。首次公开发布使用全新 Git 历史，提交邮箱使用 GitHub noreply 地址。

本仓库的发布验证覆盖文档结构、示例格式与脱敏检查。实际账号更新需要浏览器会话与用户提供的目标值；本仓库不附带账号数据或真实运行记录。
