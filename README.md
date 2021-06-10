# 开荒一个flask写的博客后端
- [x] 2021.1.26 重新开始熟悉python和flask
- [x] 2021.2.21 做一个验证数据库完整性的装饰器
- [x] 2021.2.22 这个装饰器只用在了/hello/test上，现在要全面启用，所有orm操作都需要用上
- [x] 2021.2.23 所有orm操作都要改造，因为session、table class的位置都变了
- [x] 2021.2.23 reqparse.RequestParser()要不要做在一个文件里，然后其他文件来引用，这样也许能降低内存：试过了，发现会报错
- [x] 2021.2.25 对接login接口存在问题，前端的post已经接通，可以设置token，但是用get方法把token传递给后端时没有接通，是因为get方法的接口还没有修改。但是前端已经定义了两种角色：admin-token和editor-token，需要在后端的表里做修改
- [x] 2021.2.25 问题出在前端没有成功保存cookie，原因是因为前端调用了清除cookie的接口
- [x] 2021.3.1 继续寻找调用清除cookies的代码，正在捋清调用顺序
- [x] 登录组件
- [x] 2021.3.2 验证用户名是否重复的接口
- [x] 2021.3.8 上传头像，并且修改数据库的接口。要保证验证token。前端修改头像后形成的是blob文件，用post传到后端，发现后端接收不到。可以尝试在前端把blob转成png后再传到后端
- [x] 2021.3.21 后端在token里赋值user的id，但前端没有接收到
- [x] 2021.3.22 后端接收头像后，生成文件夹
- [x] 2021.3.31 新问题，如果给avatar命名添加时间戳，那就会无限新增文件，除非在上传后清空文件夹
- [x] 2021.3.31 修改头像，完成
- [x] 2021.3.31 后端返回token的地方有好几个，万一以后新增token的字段，要修改的地方也有好几处，要做一个外接接口。2021.4.1尝试用flask_restful fields失败了，可能因为加密时二次jsonify的原因，fields不能二次jsonify。
- [x] 2021.3.31 修改用户名，并修改前端token
- [x] 2021.4.6 user list。
- [x] 2021.4.6 首先要规范数据库user表的字段
- [ ] 2021.4.7 user list 差博客数量
- [ ] 2021.4.7 user list 页的操作功能，点击以后进入到该用户的编辑页。
- [x] 2021.4.7 编辑用户页，查询某个已存在的用户时，在头像框显示头像
- [x] 2021.4.19 继续完善编辑用户页，目前剩余编辑电话和编辑权限
- [x] 2021.4.6 新增用户页，记得先给一个默认头像。
- [x] 2021.4.27 文章list页，后端要先改造数据库。用alembic管理数据库版本，目前添加了article表和user表的外键，还没有升级版本，要修改升级配置文件。
- [x] 2021.5.2 采用vditor作为编辑器。
- [x] 2021.5.26 用vditor保存文章。（1、修改数据库，新增article表）
- [x] 2021.5.26 要在后端生成md，而不能从前端传送md文件。所以要先修改后端，达到生成md的效果。
- [x] 2021.5.26 前端api接口和后端对应起来，在markdown组件里修改。
- [x] 2021.5.10 使用lute在前端解析md格式的文件。
- [x] 2021.4.1 编辑文章，采用图库形式
- [ ] 2021.6.11 根据articleID返回这篇文章的信息
- [ ] 2021.6.11 设置查看和修改权限，除非是管理员或者文章作者，否则不能看到和修改这篇文章
- [ ] 2021.5.10 vditor上传图片验证token，vditor自带token功能
- [ ] 2021.4.1 使用flasl_upload库
- [ ] 2021.3.31 前端api的斜杠问题不统一
- [ ] 2021.3.31 后端修改avatar的端口会返回data，前端不知道用不用得到
- [ ] 2021.4.19 创建一个验证x-token的装饰器，先验证通过，然后再调用get或post方法
- [ ] 邮箱验证码注册。目前还要给验证码设置有效期。验证码用协程
- [ ] 邮箱验证码登录
- [ ] github登录后获取头像和名字，绑定邮箱