![Picup](https://raw.githubusercontent.com/yiqf/Picup/master/Picup.png)

本软件主要实现WebDav服务器的文件上传，以完成与Markdown文档的对接。  
  
仅为方便个人使用，未经授权，请勿转载和传播!  
  
此软件仅作为学习交流使用，不用于任何商业用途。

## 使用说明
### 上传区

#### 文件上传

- **主视图上传区**
	- 拖拽上传
	- 剪切板上传
	- 选择文件上传
	- url上传
- **快捷上传**
	- **【剪切板】**：当图片文件或路径位于剪切板时，可选择此按钮上传
	- **【url】**：当剪切板为图片链接时，可选择此按钮上传

#### 文件链接

- 上传成功后，会自动复制链接到剪切板
- 可以点击 **【复制】** 按钮手动复制链接

### 参数配置

#### 存储配置

- **链接地址**：webdav上传地址，包含域名、端口、路径的完整地址
- **账号**：连接时的账号
- **密码**：连接时的密码
- **自定义域名**：返回的链接路径

#### 上传配置

- **图像压缩**：图像压缩方式
	- 只有图像会进行压缩，上传其他格式的文件时，请关闭此功能
	- 暂不提供图像压缩功能
	- 如有需要可继承*picup.compress.base.CompressBase*类实现功能
	- 推荐压缩方式不超过3个，不然排版可能出现问题
- **自动重命名**：上传时自动重命名文件
	- 默认重命名为：`%Y%m%d%H%M%S-{uuid}`
- **配置操作**
	- **【保存配置】**：默认保存位置config/account.yaml
		- 当加密选项开启，密钥不存在时，会自动创建密钥
	- **【读取配置】**：默认读取位置config/account.yaml

## 配置文件

### config.yaml

```yaml
resource:  
  path: resource  # 资源文件夹名称
useragent:  
  filename: fake_useragent_0.1.11.json 
account:  
  filename: account.yaml  # 用户信息文件夹名称，默认位置config/account.yaml 
  username:  
    encrypt: true  # 用户名加密开关
  password:  
    encrypt: true  # 密码加密开关
```

### account.yaml

```yaml
address: https://127.0.0.1:8888/path # 路径
custom_link: https://1.1.1.1:6666/path  # 自定义链接
username: username # 账号
password: password # 密码
compress: close # 压缩方式
rename: true # 自动重命名
rename_text: '%Y%m%d%H%M%S-{uuid}' # 重命名格式
```