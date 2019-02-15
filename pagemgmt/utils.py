# coding=utf-8
from models import Page, Comment


def init_pages():
    if Page.objects.count()==0:
        Page.objects.bulk_create([
            Page(title='安全内控与项目管理平台上线了',
                 content='''安全内控与项目管理平台上线了!<br>
                    安全内控与项目管理平台旨在提供一个保障产品安全的项目管理流程。 ''',
                 author='Jane',
                 pseudo_name='sdl-online',
                 keywords='安全内控与项目管理平台',
                 description='安全内控与项目管理平台上线'),
            Page(title='什么是SDL',
                 content='''SDL, Security Development Cycle(安全开发周期)。<br>
                 它从源头开始进行安全控制，通过规范的项目管理过程和关键安全任务的引入，确保开发设计及部署过程中遵从安全标准与规范，保障所交付产品在全生命周期过程中的安全性。<br>
                ''',
                 author='Jane',
                 pseudo_name='sdl',
                 keywords='SDL',
                 description='安全开发周期定义'),
        ])
    return


def create_comment(_page, current_user, _content):
    Comment.objects.create(page=_page, commenter=current_user, content=_content)
    return
