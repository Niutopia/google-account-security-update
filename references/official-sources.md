# Google 官方资料与行为边界

核实日期：2026-11-23。以下链接为 Google 官方帮助；界面名称、选项与适用条件可能随账号类型、地区、设备或产品版本变化。中文步骤用于执行，链接保留实际核查的英文版本。

## 设置入口

优先从已核对身份的账号页面进入目标项目，多账号场景不要依赖固定的账号索引。

| 项目 | 入口 |
|---|---|
| 账号首页 | <https://myaccount.google.com/> |
| 安全设置 | <https://myaccount.google.com/security> |
| Authenticator | <https://myaccount.google.com/two-step-verification/authenticator> |
| 通行密钥 | <https://myaccount.google.com/signinoptions/passkeys> |

直接入口可能要求重新验证身份；重定向后再次核对账号。

## 恢复邮箱与恢复电话

[Set up recovery options](https://support.google.com/accounts/answer/183723?hl=en)

- 通常位于 Security & sign-in → How you sign in to Google → Recovery email / Recovery phone，可能要求再次登录。
- 恢复邮箱应是经常使用且不同于此账号登录邮箱的地址；恢复电话应能接收短信并由账号使用者掌控。
- 更改恢复信息或其他身份验证因素后，Google **可能在之后 7 天内继续向旧信息发送验证码**。这是可能性，不代表旧信息一定可用，也不代表仅靠旧信息即可完成恢复。
- 恢复电话与其他 Google 服务中使用的号码有不同用途，修改或删除一处不等于同步修改所有用途。
- 编辑选项可能因登录环境变化而暂时不可用；官方建议使用常用设备/地点，或下周在当前设备重试。组织账号还可能受管理员设置影响。

[How to recover your Google Account or Gmail](https://support.google.com/accounts/answer/7682439?hl=en)

- 恢复信息变更可能需要最长 7 天才生效。这与“旧信息可能继续收到验证码”的窗口分别记录。

## Authenticator 与两步验证

[Get verification codes with Google Authenticator](https://support.google.com/accounts/answer/1066447?hl=en&co=GENIE.Platform%3DAndroid)

- 在账号的 Authenticator 设置页按屏幕指引配置。公共帮助未规定所有账号都使用相同的“更换”按钮名称。
- 手机之间同步或导入验证码，与在 Google 账号端重新配置密钥，是两种操作。导入成功不代表旧设备上的副本已撤销。
- 若账号设置流程要求验证码，使用新配置产生的当前码，以 Google 页面接受并完成登记为依据。
- 码不匹配时检查账号、服务、有效期及系统时间。Authenticator 7.0 起使用操作系统时间，应用内不再提供旧版时间校正设置。
- 新设置的 Authenticator 可能需要最长 7 天才在登录时显示为可选方式；绑定完成不等于立即在所有挑战中出现。
- 该公共帮助未明确保证重新配置时旧密钥的具体失效时点，不据此声明所有旧副本已失效。

[Turn on 2-Step Verification](https://support.google.com/accounts/answer/185839?hl=en)

- 两步验证是账号级设置。以总览当前启用状态为准，组织账号可能由管理员控制。

[Sign in with backup codes](https://support.google.com/accounts/answer/1187538?hl=en)

- 需先启用两步验证。备用验证码一次性使用；生成新一组时旧一组失效。
- 该功能与下载选项受账号配置影响。只在用户指定时生成并保存在其私密存储。

## 通行密钥

[Sign in with a passkey instead of a password](https://support.google.com/accounts/answer/13548313?hl=en)

- 创建需要支持的设备/浏览器及屏幕锁。按当前官方条件，iPhone、iPad 和 macOS 应开启 iCloud Keychain；使用手机上的通行密钥登录另一台电脑时，应开启蓝牙。
- 只在账号使用者控制的设备或硬件安全密钥上创建。设备解锁权限直接影响通行密钥的使用。
- 添加通行密钥不会自动删除其他验证方式和恢复方式。
- 新建通行密钥可能需要等待 7 天才可用于登录；组织账号是否支持仅凭通行密钥登录取决于管理员设置。
- 创建成功、Google 列表存在、本轮用它通过挑战，分别记录。

## 密码、设备会话与应用专用密码

[Change or reset your password](https://support.google.com/accounts/answer/41078?hl=en)

- 常见路径为 Security & sign-in → How you sign in to Google → Password；可能要求再次登录。
- 修改或重置密码后会退出多数登录，但官方列出例外：用于验证登录身份的设备、部分已获准访问账号的第三方应用所在设备，以及已获准访问的家用智能设备。

[See devices with account access](https://support.google.com/accounts/answer/3067630?hl=en)

- 同一设备可能存在多个会话。设备列表还包含近期登录过的设备，应读取 Signed out 等状态，避免把历史列表项当作当前登录。
- 用户要求退出某设备时，按实际列表检查该设备的相关会话；只改密码不等于已执行全部会话清理。

[Sign in with app passwords](https://support.google.com/accounts/answer/185833?hl=en)

- **修改 Google 账号密码时，已有应用专用密码会被撤销。** 仍使用它的应用可能需要重新配置。
- 应用专用密码要求开启两步验证；组织账号、仅安全密钥配置或高级保护等情况可能没有该选项。
- 此规则不等于所有 OAuth / “使用 Google 登录”授权都被撤销。

## 额外确认、等待与恢复

[Verify it's you to complete a sensitive action](https://support.google.com/accounts/answer/7162782?hl=en&co=GENIE.Platform%3DDesktop)

- 敏感操作可能要求使用已关联一段时间的设备、电话或安全密钥；显示 Sensitive action blocked 时可能涉及 7 天限制。
- 该等待条件不同于新恢复信息生效窗口，也不应套用到每一种验证码失败。

[Fix common issues with 2-Step Verification](https://support.google.com/accounts/answer/185834?hl=en)

- 多次请求短信等验证码时，使用最后一次请求对应的验证码，不要仅按短信到达顺序判断；这项规则不要泛化为 TOTP 的通用轮换语义。
- 缺少第二步方式而进入恢复时，时间与普通设置操作不同，应跟随具体页面提示。

[Tips to complete account recovery steps](https://support.google.com/accounts/answer/7299973?hl=en) · [Why your account recovery request is delayed](https://support.google.com/accounts/answer/9412469?hl=en)

- 恢复时优先使用常用设备、浏览器和地点；恢复请求可能因具体情况等待数小时或若干天。
- 官方帮助没有给普通设置操作一个统一的每小时次数或“输错验证码后一律等待若干小时”的保证。按实际页面提示记录，不编造固定频率或解锁时长。

本 Skill 的单次挑战一次提交、逐项回读及串行处理，是操作约定，不是 Google 官方公布的统一速率上限。
