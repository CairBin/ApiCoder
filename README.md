# ApiCoder

## 描述
三层分层设计的.Net6.0 WebApi项目的代码生成脚本。
本项目生成的代码默认使用了SqlSugar以及SqlSugar.IOC的包，并添加了相关的`using`引用。

## 使用

### 以Python脚本的形式运行

* Linux
```shell
python3 main.py JSON文件 -o 输出目录
```

* Windows
```bash
py main.py JSON文件 -o 输出目录
```

文件生成后，需要将其添加到您的C#项目中。
代码文件默认连接的数据库类型为MySQL，可于Program.tmp模板文件SqlSugar IOC Settings部分修改相关配置。

当您将代码文件导入项目后，须在C#项目的**appsettings.json**文件中追加名称为`SqlConnString`的数据库连接字符串,MySql写法如下所示
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "SqlConnString": "server=数据库地址;user=用户名;password=密码;port=端口号默认3306;database=数据库名称"
}

```

## 配置文件
通过编写配置文件来生成.Net6.0 WebApi项目模型层、仓储层、服务层以及IOC注入相关的C#代码文件

配置文件规范如下方所示
```json
{
    "template":"template/default/",
    "namespace":"HelloWorld.Api",
    "BaseModel":{
        "enable":true,
        "classname":"BaseId",
        "type":{
            "Id": "int"
        }
    },
    "model":[
        {
            "classname":"yourclassname",
            "type": {
                "Name1":"type1",
                "Name2":"type2"
            },
            "inherit": true
        }
    ]
}
```
* `template`  为模板目录
* `namespace` 为项目名称，一般用于填充命名空间的一部分
* `BaseModel` 为描述模型层基类的对象
    * `enable` 为是否启用该基类的标志，如果为`false`则会使其它模型`inherit`无效
    * `classname` 为基类类名
    * `type` 其成员描述组成基类的数据类型，前面为名称，后面为C#类型
* `model` 其成员描述除基类以外的其它实体，用于创建数据库表单
    * `inherit` 是否继承基类

具体用法可参考自带的config.json文件。


## 替换标签
这些标签存在于模板文件中

```
<namespace> 项目名称，允许存在于任何模板文件。
<type> 模型层目录树中的类型，仅允许存在于Model.tmp。
<fatherclass> 模型层继承的基类，前面要跟分号，例如 ':BaseId'。仅允许存在于Model.tmp。
<typename> 模型层类名，允许存在于除IocExtend.tmp以及Base相关的模板文件中。
<sertype> IOC注入语句，仅允许存在于IocExtend.tmp
<inittype> 创建数据库表单的语句，仅允许存在于BaseRepository.tmp
```

## 模板文件
默认的模板文件于`template\default\`目录下，其内容如有需求可自行编写。

* `BaseModel.tmp` 基类模板
* `Model.tmp` 其它实体模板
* `InterfaceBaseRepository.tmp` 基础仓储接口模板
* `BaseRepository.tmp` 基础仓储模板
* `InterfaceRepository.tmp` 实体相关的仓储层接口模板
* `Repository.tmp` 实体相关的仓储层模板
* `InterfaceBaseService.tmp` 服务层基础接口模板
* `BaseService.tmp` 基础服务模板
* `InterfaceService.tmp` 实体相关的服务层接口模板
* `Service.tmp` 实体相关的服务层模板
* `IocExtend.tmp` 定义了Ioc注入等相关操作的类的模板
* `Program.tmp` 用于生成Program.cs文件，在自带的基础上调用了IocExtend中的一些方法，对SqlSugar Ioc做了配置

## 可维护性
这个脚本一开始只是想拿来临时使用，设计的时候没想那么多，可维护性也比较差，项目会不定期维护。（狗头保命）