import sys
import tools
import define



def settings(config):
    define.tmp_path = config['template']
    if define.tmp_path[-1] != '/':
        define.tmp_path += '/'

    define.output_path = config['output']
    if define.output_path[-1] != '/':
        define.output_path += '/'
    
    define.namespace = config['namespace']
    define.base_model = config['BaseModel']
    define.models = config['model']
    for i in config['model']:
        define.names.append(i['classname'])

    define.output_path += define.namespace + '/'

    define.model_output_path = define.output_path+'Model/'
    if not tools.check_dir(define.model_output_path):
        tools.make_dir(define.model_output_path)

    define.rep_output_path = define.output_path+'Repository/'
    if not tools.check_dir(define.model_output_path):
        tools.make_dir(define.rep_output_path)

    define.ser_output_path = define.output_path+'Service/'
    if not tools.check_dir(define.ser_output_path):
        tools.make_dir(define.ser_output_path)

    # services.AddScoped<InterfaceFriendsInfoRepository, FriendsInfoRepository>();
    for n in define.names:
        define.init_str += 'typeof('+n+'),\n\t\t\t\t'
        define.ser_str += 'services.AddScoped<'+define.interface + n+define.rep_tmp_name+', ' + n+define.rep_tmp_name+'>();\n\t\t\t'

def build(readpath, obj,outpath):
    data = tools.read_file(readpath)
    data = data.replace('<namespace></namespace>', define.namespace)
    if obj != None:
        type_str = ''
        for i in obj['type']:
            type_str += 'public ' + obj['type'][i] + ' ' + i + ' {get;set;}\n\t\t'
        data = data.replace('<type></type>', type_str)
        data = data.replace('<typename></typename>', obj['classname'])
        if obj['inherit'] and define.base_model['enable']:
            data = data.replace('<fatherclass></fatherclass>',
                     ':'+define.base_model['classname'])
    else:
        data = data.replace('<inittype></inittype>', define.init_str)
        data = data.replace('<sertype></sertype>', define.ser_str)

    tools.write_file(outpath,data)

def run():
    if define.base_model['enable']:
        data = data = tools.read_file(
            define.tmp_path + define.basemodel_tmp_name + '.tmp')
        data = data.replace('<namespace></namespace>', define.namespace)
        data = data.replace('<typename></typename>', define.base_model['classname'])
        temp = ''
        for i in define.base_model['type']:
            temp += 'public ' + define.base_model['type'][i] + ' ' + i + ' {get;set;}\n\t\t'
        data = data.replace('<type></type>', temp)
        tools.write_file(define.model_output_path +
                         define.base_model['classname']+'.cs', data)
    
    build(define.tmp_path+define.ibaserep_tmp_name + '.tmp', None, define.rep_output_path + define.ibaserep_tmp_name + '.cs')
    build(define.tmp_path+define.baserep_tmp_name + '.tmp', None, define.rep_output_path + define.baserep_tmp_name + '.cs')
    build(define.tmp_path+define.ibaseser_tmp_name+'.tmp', None, define.ser_output_path + define.ibaseser_tmp_name + '.cs')
    build(define.tmp_path+define.baseser_tmp_name+'.tmp', None, define.ser_output_path + define.baseser_tmp_name + '.cs')

    for m in define.models:
        build(define.tmp_path+define.model_tmp_name+'.tmp', m, define.model_output_path+m['classname']+'.cs')
        build(define.tmp_path+define.interface+define.rep_tmp_name+'.tmp',m,define.rep_output_path+define.interface+m['classname']+define.rep+'.cs')
        build(define.tmp_path+define.rep_tmp_name+'.tmp', m, define.rep_output_path+m['classname']+define.rep+'.cs')
        build(define.tmp_path+define.interface+define.ser_tmp_name+'.tmp',m,define.ser_output_path+define.interface+m['classname']+define.ser + '.cs')
        build(define.tmp_path+define.ser_tmp_name+'.tmp', m,define.ser_output_path+m['classname']+define.ser + '.cs')

    build(define.tmp_path+'IocExtend.tmp', None, define.output_path+'IocExtend.cs')
    build(define.tmp_path+'Program.tmp',None, define.output_path+'Program.cs')

def param(argv,length):
    if argv[1]== '-h':
        print(define.des)
    elif argv[1] == '-v':
        print('v1.1.0')
    else:
        if length < 3:
            print("缺少必要参数，您是否需要键入-h以获得帮助")
        else:
            if not tools.check_dir(argv[3]):
                tools.make_dir(argv[3])
            else:
                config = tools.read_json(argv[1])
                config.update({'output':str(argv[3])})
                settings(config)
                run()

if __name__ == '__main__':
    len_argv = len(sys.argv)
    if len_argv <= 1:
        print("缺少必要参数，您是否需要键入-h以获得帮助")
    else:
        param(sys.argv,len_argv)