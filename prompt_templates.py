prompt_paper_sum = {
    "en": """
    Write a concise summary of the paper with the following format, summarise the conclusion into points:
    '''
    1. Title:
    2. Authors:
    3. Research Topics:
    4. Research Method:
    5. Data Source:
    6. Conclusion:
        (1)
        (2)
        ...
    '''

    The text need to be summarized:
    "{text}"

    CONCISE SUMMARY:""",

    "cn": """
    请使用中文将论文的内容按照以下格式进行总结: 
    '''
    1. 题目:
    2. 作者:
    3. 研究主题:
    4. 研究方法:
    5. 数据来源:
    6. 结论:
        (1)
        (2)
        ...
    '''

    需要被总结的论文文本: 
    "{text}"

    简要总结:"""
}

prompt_sum_translate = {
    "en": """
    Translate the following text into English without changing the format:

    {text}
    """,

    "cn": """
    请将下面的文字翻译成中文且不修改其格式:

    {text}
    """
}
