from argparse import ArgumentParser

from lagent.actions import ActionExecutor, IPythonInterpreter, Image2VideoInterpreter, TableQAInterpreter
from lagent.agents.internlm2_agent import INTERPRETER_CN, META_CN, PLUGIN_CN, Internlm2Agent, Internlm2Protocol
from lagent.llms import HFTransformer
from lagent.llms.meta_template import INTERNLM2_META as META
from lagent.schema import AgentStatusCode

import torch

def parse_args():
    parser = ArgumentParser(description='chatbot')
    parser.add_argument(
        '--path',
        type=str,
        default='/share/model_repos/internlm2-chat-7b',
        help='The path to the model')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    # Initialize the HFTransformer-based Language Model (llm)
    model = HFTransformer(
        path=args.path,
        meta_template=META,
        top_p=0.8,
        top_k=None,
        temperature=0.1,
        repetition_penalty=1.0,
        stop_words=['<|im_end|>'])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    plugin_executor = ActionExecutor(actions=[Image2VideoInterpreter(device), TableQAInterpreter(device)])  # noqa: F841
    interpreter_executor = ActionExecutor(actions=[IPythonInterpreter()])

    chatbot = Internlm2Agent(
        llm=model,
        plugin_executor=plugin_executor,
        interpreter_executor=interpreter_executor,
        protocol=Internlm2Protocol(
            meta_prompt=META_CN,
            interpreter_prompt=INTERPRETER_CN,
            plugin_prompt=PLUGIN_CN,
            tool=dict(
                begin='{start_token}{name}\n',
                start_token='<|action_start|>',
                name_map=dict(
                    plugin='<|plugin|>', interpreter='<|interpreter|>'),
                belong='assistant',
                end='<|action_end|>\n',
            ),
        ),
    )

    def input_prompt():
        print('\ndouble enter to end input >>> ', end='', flush=True)
        sentinel = ''  # ends when this string is seen
        return '\n'.join(iter(input, sentinel))

    history = []
    while True:
        try:
            prompt = input_prompt()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            continue
        if prompt == 'exit':
            exit(0)
        history.append(dict(role='user', content=prompt))
        print('\nInternLm2：', end='')
        current_length = 0
        last_status = None
        for agent_return in chatbot.stream_chat(history, max_new_tokens=2048):
            status = agent_return.state
            if status not in [
                    AgentStatusCode.STREAM_ING, AgentStatusCode.CODING,
                    AgentStatusCode.PLUGIN_START
            ]:
                continue
            if status != last_status:
                current_length = 0
                print('')
            if isinstance(agent_return.response, dict):
                action = f"\n\n {agent_return.response['name']}: \n\n"
                action_input = agent_return.response['parameters']
                if agent_return.response['name'] == 'IPythonInterpreter':
                    action_input = action_input['command']
                response = action + action_input
            else:
                response = agent_return.response
            print(response[current_length:], end='', flush=True)
            current_length = len(response)
            last_status = status
        print('')
        history.extend(agent_return.inner_steps)


if __name__ == '__main__':
    main()


# 请使用表格分析工具，表格路径为/root/code/table.csv。问题：表格中最大的年龄是多少？
# 请使用表格分析工具，表格路径为/root/code/table.csv。问题：表格中平均年龄是多少？