# 来源与维护说明

本页由 AI Music Maker 团队维护。本次核对日期：2026-09-23。

## 内容依据

| 内容 | 来源 | 使用边界 |
| --- | --- | --- |
| 品牌定位、工具入口、运营主体 | [AI Music Maker 官网](https://musicmaker.im/) | 官网产品说明，不是独立评测；没有进行音频或视频生成实测 |
| 全部官网语言 | 官网 HTML 的 `hreflang` 与页脚语言列表 | 英语、日语、印尼语、意大利语、葡萄牙语、西班牙语、德语、俄语、法语、简体中文、繁体中文、韩语、泰语、越南语、阿拉伯语，共 15 种 |
| 公开项目及用途 | [品牌仓库列表](https://github.com/orgs/aimusicmaker/repositories)、[歌曲指南](https://github.com/aimusicmaker/awesome-suno-creator-guide)、[音乐视频指南](https://github.com/aimusicmaker/awesome-music-video-creator-guide) | 项目介绍依据 README；不把引用案例写成团队实测或模型官方背书 |
| 首页组织方式 | [FLAQ GitHub 主页](https://github.com/flaqai) | 参考品牌定位、开源动机、项目用途、产品入口、参与合作的阅读顺序；不移植 FLAQ 的数量、履历或产品能力 |
| 联盟合作 | [联盟计划](https://musicmaker.im/affiliate-program/)、[联盟协议](https://musicmaker.im/affiliate-agreement/) | 首笔有效付费订单 20%，注册后 60 天内后续有效付费订单 10%；资格、归因、退款、拒付和现行协议决定结算 |
| 商用与价格 | [商用许可](https://musicmaker.im/commercial-license/)、[套餐](https://musicmaker.im/pricing/)、[服务条款](https://musicmaker.im/terms-of-service/) | 首页不自行扩大授权范围，不承诺全部免费或版权无风险 |
| 内容审查依据 | [Google：以用户为中心的实用、可靠内容](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | 检查经验、专业性、权威性、可信度；这些不是单一排名因素，也不是可认证的分数 |

## 维护方法

- `profile/README.md` 是英文组织首页；其余 14 份 `profile/README_*.md` 是完整语言版本。`profile/mobile/` 提供相同 15 种语言的独立手机版；页首按钮可切换桌面与手机视图，语言切换保持当前视图。根目录 README 同步英文内容，便于仓库访问者阅读。
- 修改 `i18n/*.json`，再运行 `python3 scripts/build_profile.py`。不要只改生成文件。
- 运行 `python3 scripts/build_profile.py --check` 与 `git diff --check`，检查生成内容是否同步及空白错误。
- 发布前核对 GitHub 仓库链接、官网入口、语言范围和联盟条款；只有实际重新核对后才更新核对日期。
- 按钮使用仓库内 SVG，避免依赖第三方徽章服务。图片链接使用本仓库的公开原始文件地址，发布后才能在 GitHub 读取。
- 指南链接定位对应语言 README。工具表格使用已核对的官网英文路径，避免假设每个工具都已有相同语言的页面；页首创作与试听按钮进入相应语言路径。
- 组织首页配图复用本品牌两份指南的原创插画；原始文件、用途及 MIT 许可见 [配图来源](../assets/CREDITS.md)。未变更其他项目的许可证。
