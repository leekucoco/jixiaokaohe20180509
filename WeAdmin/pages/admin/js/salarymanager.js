layui.use('table', function(){

    var table = layui.table;
    token = window.localStorage.getItem('token');
    token =  "JWT " + token;
    table.render({
        elem: '#salarymanage'
        ,url:'https://dqrcbankservice.com:8001/api/salaryrecord/'
        ,height: 'full-200'
        ,page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
            layout: ['limit', 'count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
            //,curr: 5 //设定初始在第 5 页
            ,groups: 3 //只显示 1 个连续页码
            ,first: false //不显示首页
            ,last: false//不显示尾页
        }
        ,headers: {
            Authorization:token
        }
        ,response: {
            statusName: 'status' //数据状态的字段名称，默认：code
            ,statusCode: 200 //成功的状态码，默认：0
            // ,msgName: 'hint' //状态信息的字段名称，默认：msg
            ,countName: 'count' //数据总数的字段名称，默认：count
            ,dataName: 'results' //数据列表的字段名称，默认：data
        }
        // ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
        ,cols: [[
            {type:'checkbox', fixed: 'left'}
            // ,{field:'id',  wide:80, sort: true, title:"工资记录id"}
            // ,{field:'add_time',  wide:80, sort: true, title:"记录添加时间"}
            ,{field:'id', width:60,title:"ID"}
            ,{field:'date',width:120, title:"添加时间"}
            ,{field:'extrainfo',width:120,sort: true,title:"备注信息"

             }
             ,{field:'checkonworkfile',width:120, title:"病假事假记录"
                ,templet: function (d) {
                    if (d.checkonworkfile != null){
                        return "已上传"
                    }else{
                        return "未上传"
                    }
                 }

            }
             ,{field:'baseandwelfareaddfile',width:120,  title:"补发基本福利薪酬记录"
                ,templet: function (d) {
                    if (d.baseandwelfareaddfile != null){
                        return "已上传"
                    }else{
                        return "未上传"
                    }
                 }
            }
             ,{field:'insuranceandfundfile',width:120,  title:"五险一金记录"
                ,templet: function (d) {
                    if (d.insuranceandfundfile != null){
                        return "已上传"
                    }else{
                        return "未上传"
                    }
                 }
            }

             ,{field:'taxandotherdeductionfile',width:120,  title:"税费及其他扣除项记录"
                ,templet: function (d) {
                    if (d.taxandotherdeductionfile != null){
                        return "已上传"
                    }else{
                        return "未上传"
                    }
                 }
             }

              ,{field:'status',width:100,  title:"工资记录状态"
                ,templet: function (d) {
                    if (d.status == "LOCK"){
                        return "已经封账"
                    }else if(d.status == "SENDMSG"){
                        return "短信已发"
                    }else if(d.status == "UNCOMPELTE"){
                        return "取消封账"
                    }else{
                        return "未封账"
                    }

                 }
            }

             ,{field:'right', width:100 , title:"可选操作", toolbar: '#barDemo'}
        ]]
        ,id: 'testReload'
    });



    //监听表格复选框选择
    table.on('checkbox(salarydemo)', function(obj) {
        console.log(obj)
    });
    table.on('edit(salarydemo)', function(obj){

            var value = obj.value //得到修改后的
            ,data = obj.data //得到所在行所有键值
            ,field = obj.field;//得到字段
        layer.msg('[ID: '+ data.ID +'] ' + field + '字段更改为:'+ value);

    });
    //监听工具条
    table.on('tool(salarymanagedem)', function(obj){
        var data = obj.data;
        console.log(data)
        var msg = ""
        var html = '<div class="layui-form">'+
            '<table class="layui-table" id="certable">'+
            '<colgroup> <col width="150"> <col width="150"> <col width="300"> <col> </colgroup>'+
            '<thead> <tr> <th>证书名称</th> <th>证书得分</th> <th>证书图片</th></tr> </thead><tbody>'
        if(obj.event === 'detail'){
            if(data.certificates != 'no certificates info'){
                for (i = 0; i<data.certificates.length; i++){
                    html = html+"<tr> <td>"+data.certificates[i].name+
                        "</td> <td>"+data.certificates[i].score+
                        "</td> <td><img src="+ data.certificates[i].image + " >"+"</td></tr>"
                   // msg = msg + data.certificates[i].certificate
                }
            }else{
                html = html +"<tr> <td>证书信息不存在</td></tr>>"
            }
            //layer.msg('ID：'+ data.ID + ' 的查看操作'+data.certificates[0].certificate);

            layer.open({
                type: 1,
                title: '员工证书明细',
                shadeClose: true,
                shade: false,
                maxmin: true, //开启最大化最小化按钮
                area: ['800px', '300px'],
                content: html+'</tbody> </table> </div>'
            });
        } else if(obj.event === 'del'){
            console.log(obj.data)
            layer.confirm('真的删除行么', function(index){
                layui.jquery.ajax(
                    {
                        url: '/cofficient/'+obj.data.id,
                        type: 'DELETE',
                        contentType: 'application/json;charset=utf-8',
                        //data: JSON.stringify(data),
                        error : function (res) {
                            if (res.status != 403){
                            layer.alert('未知的错我')
                             }else{
                            layer.alert('无权限操作此数据')
                         }
                        },
                        success : function (res) {
                            obj.del();
                            layer.close(index);
                        },
                        beforeSend: function(xhr) {
                            token = window.localStorage.getItem('token');
                            xhr.setRequestHeader("authorization", "JWT " + token);
                     }
                    }
                );

            });
        } else if(obj.event === 'update'){
            //console.log(obj.data)

            layui.jquery.ajax(
                {
                    url: '/cofficient/'+obj.data.id+'/',
                    type: 'PUT',
                    contentType: 'application/json;charset=utf-8',

                    data: JSON.stringify({
                        coefficent:parseFloat(obj.data.coefficent),
                        user:parseInt(obj.data.user)
                    }),
                    error : function (res) {
                        //console.log(res.status)
                        if (res.status != 403){
                            layer.alert('未知的错我')
                        }else{
                            layer.alert('无权限操作此数据')
                        }

                    },
                    success : function (res) {
                        //console.log(res)
                        layer.alert('更新行：<br>'+
                            '姓名:'+data.name+'<br>')
                        //obj.del();
                        // layer.close(index);
                    },
                    beforeSend: function(xhr) {
                        token = window.localStorage.getItem('token');
                         xhr.setRequestHeader("authorization", "JWT " + token);
                     }
                }
            );

        }
    });



    var $ = layui.$, active = {
        getCheckData: function(obj,index){ //获取选中数据
            var checkStatus = table.checkStatus('salarydetail')
                ,data = checkStatus.data;
            layer.confirm('真的删除行么', function(index) {
                //  layer.alert(JSON.stringify(data));
                for (i = 0; i < data.length; i++) {
                    layui.jquery.ajax(
                        {
                            url: '/api/v1/delstaffrecord',
                            type: 'DELETE',
                            contentType: 'application/json;charset=utf-8',
                            data: JSON.stringify(data[i]),
                            error: function (res) {
                                layer.alert(res);
                            },
                            success: function (res) {
                                //checkStatus.index
                                console.log(res)

                            }
                        }
                    );
                }
                layer.close(index);
                table.reload('salarydetail');
            });

        }
        ,getCheckLength: function(){ //获取选中数目
            var checkStatus = table.checkStatus('salarydetail')
                ,data = checkStatus.data;
            layer.msg('选中了：'+ data.length + ' 个');
        }
        ,isAll: function(){ //验证是否全选
            var checkStatus = table.checkStatus('salarydetail');
            layer.msg(checkStatus.isAll ? '全选': '未全选')
        }
    };

    $('.demoTable .layui-btn').on('click', function(){
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
    $('.demoTable .layui-btn').on('click', function(){
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});


function searchsalarydetailbytime() {
    var addtime0 = layui.jquery("#start").val();
    var addtime1 = layui.jquery("#end").val();
    //console.log(addtime0,addtime1);
    var table = layui.table;
    table.reload('testReload',{

        url:'https://dqrcbankservice.com:8001/api/fsalary/?add_time_0='+addtime0+"&add_time_1="+addtime1
      // where: { //设定异步数据接口的额外参数，任意设
      //       search: 'data'
      //
      //       //…
      //     }
          ,page: {
            curr: 1 //重新从第 1 页开始
          }
    })

}

function PWeAdminEdit() {
    var table = layui.table;
    table.on('tool(salarymanagedemo)', function(obj){ //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
        var data = obj.data; //获得当前行数据
        //console.log(typeof(data))
        datajsonstr = JSON.stringify(data);
        WeAdminEdit('编辑','./edit.html',datajsonstr)
  })
}

function Delsrecord() {
    var table = layui.table;
    table.on('tool(salarymanagedemo)', function(obj){ //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
        var data = obj.data; //获得当前行数据
        console.log(obj)
        //datajsonstr = JSON.stringify(data);
         layui.jquery.ajax(
            {
                url: 'https://dqrcbankservice.com:8001/api/salaryrecord/'+data.id,
                type: 'DELETE',
                contentType: 'application/json;charset=utf-8',
                // data: JSON.stringify(datatosend),
                error: function (rest) {
                    if (res.status != 403){
                        layer.alert('未知错误！检查数据格式、字段名称')
                         }else{
                        layer.alert('无权限操作此数据')
                     }
                },
                success: function (rest) {
                    //obj.del();
                    // var resjson = JSON.parse(rest);
                    // successcount = resjson.successcount
                    // alertstr = "上传成功"+successcount+"条数据"
                    // layer.alert("成功删除", {icon: 6},function () {
                    //     var index = parent.layer.getFrameIndex(window.name);
                    //      //关闭当前frame
                    //     parent.layer.close(index);
                    //   });
                    obj.del();
                    layer.alert("成功删除！");

                },
               beforeSend: function(xhr) {
                    token = window.localStorage.getItem('token');
                    xhr.setRequestHeader("authorization", "JWT " + token);
                }
            }
        );
  })
}

function addnewsrecord() {
        // var data = obj.data; //获得当前行数据
        // console.log(obj);
        var srecdbackupinfo = layui.jquery("#srecdbackupinfo").val();
        // console.log(srecdbackupinfo);
        //datajsonstr = JSON.stringify(data);
         layui.jquery.ajax(
            {
                url: 'https://dqrcbankservice.com:8001/api/salaryrecord/',
                type: 'POST',
                contentType: 'application/json;charset=utf-8',
                data: JSON.stringify({
                        extrainfo:srecdbackupinfo,

                    }),
                error: function (rest) {
                    if (res.status != 403){
                        layer.alert('未知错误！检查数据格式、字段名称')
                         }else{
                        layer.alert('无权限操作此数据')
                     }
                },
                success: function (rest) {

                    layer.alert("成功增加本月工资记录！");
                        var table = layui.table;
                        table.reload('testReload',{
                        url:'https://dqrcbankservice.com:8001/api/salaryrecord/'
                      // where: { //设定异步数据接口的额外参数，任意设
                      //       search: 'data'
                      //
                      //       //…
                      //     }
                          ,page: {
                            curr: 1 //重新从第 1 页开始
                          }
                    })

                },
               beforeSend: function(xhr) {
                    token = window.localStorage.getItem('token');
                    xhr.setRequestHeader("authorization", "JWT " + token);
                }
            }
        );
}
