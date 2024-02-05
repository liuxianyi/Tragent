# Tragent 智能体

[Tragent](https://github.com/liuxianyi/Tragent.git)是基于InternLM的lagent， 在lagent的基础之上添加了Transformers库中相关的开源模型，让大语言模型（如InternLM等）能够处理各类真实场景下的任务，包括自然语言处理任务、计算机视觉、多模态、语音等。

# 进度

# 路线图

- [x]  表格问答插件
- [ ]  文本生成图像插件
- [ ]  文本生成视频插件

# 运行环境

## Conda

[env.yaml](env.yaml)

## Install lagent2
```shell
git clone https://github.com/liuxianyi/lagent.git
cd lagent
pip install .
```

# Run on command line

```shell
cd Tragent
python cli_demo.py \
    --path "your internlm2 model weights or model id"
```

# Run on Gradio UI
```
```

# OpenXlab Demo


# 鸣谢

- 上海人工智能实验室 [InternLM(书生·浦语) 模型](https://github.com/InternLM/InternLM)，以及提供的A100显卡资源！
- HuggingFace，提供开源平台
- 所有开源模型的作者们