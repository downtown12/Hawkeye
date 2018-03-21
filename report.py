#encoding=utf-8
import os
from jinja2 import Environment, FileSystemLoader
from utils import leakage_col, query_col, blacklist_col, notice_col

template_dir = os.path.join(os.path.abspath('.'), 'templates/reports')
# 设置jinja2的环境
env = Environment(loader = FileSystemLoader(template_dir))

#读取模板文件
report  = env.get_template('report.html')


def render_top_items(top_nums, report_path):
    if top_nums < 0:
        #设置top_nums的默认值
        top_nums = 5
    tag_keyed_leakages = dict()
    for q in query_col.find():
        #print(q['tag'])
        tag_keyed_leakages[q['tag']]=list(leakage_col.find({'tag':q['tag']}))[:top_nums]
    html = report.render(tag_keyed_leakages = tag_keyed_leakages)
    
    with open(report_path, 'wb') as handle: 
        handle.write(html.encode('utf-8'))

def render_items_by_tags(tag_list, report_path):
    """
    render items by given tags
    """
    tag_keyed_leakages = dict.fromkeys(tag_list)
    for tag in tag_keyed_leakages.keys():
        tag_keyed_leakages[tag] = list(leakage_col.find({'tag':tag}))
        if not tag_keyed_leakages[tag]:
            del tag_keyed_leakages[tag]
    html = report.render(tag_keyed_leakages = tag_keyed_leakages)

    with open(report_path, 'wb') as handle:
        handle.write(html.encode('utf-8'))

def keyword_report(tag_list):
    """
    create keyword report html content by given tags
    """
    tag_keyed_leakages = dict()
    for tag in tag_list:
        leakages = list(leakage_col.find({'tag':tag}))
        if leakages:
            tag_keyed_leakages[tag] = leakages
    html = report.render(tag_keyed_leakages = tag_keyed_leakages)
    return html


if __name__ == "__main__":
    report_path = "./Tag_Report.html"
    tag_list = [u"直销银行", u"信用卡中心"]
    render_items_by_tags(tag_list, report_path)
