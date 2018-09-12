layui.use('table', function(){
    var table = layui.table;
    token = window.localStorage.getItem('token');
    token =  "JWT " + token;
    table.render({
        elem: '#bankuploadrecord'

        ,url:'https://dqrcbankservice.com:8001/api/bankuploadrecord/'
        ,height: '80'
        // ,page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
        //     layout: ['limit', 'count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
        //     //,curr: 5 //设定初始在第 5 页
        //     ,groups: 3 //只显示 1 个连续页码
        //     ,first: false //不显示首页
        //     ,last: false//不显示尾页
        // }
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

        ,cols: [[
            {type:'checkbox', fixed: 'left'}

            ,{field:'id', width:60,title:"ID"}

            ,{field:'depart_info',width:120,sort: true,title:"部门信息"}
            ,{field:'performancerecord_info', width:120,title:"分配记录备注"}
              ,{field:'state',width:100,  title:"记录状态"
                ,templet: function (d) {
                    if (d.state == 1){
                        return "未上传"
                    }else if(d.state == 2){
                        return "已提交审核"
                    }else if(d.state == 3){
                        return "审核未通过"
                    }else if(d.state == 4){
                        return "审核通过"
                    }else{
                        return "状态未知"
                    }
                 }
            }

             ,{field:'right', width:100 , title:"可选操作", toolbar: '#barDemo2'}
        ]]
        ,id: 'testReload'
    });

    table.render({
        elem: '#bankuploaddetail'
        ,url:'https://dqrcbankservice.com:8001/api/bankuploadrecorddetail/'
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
            ,{field:'user_name', width:100,title:"姓名"}
            ,{field:'user_username', width:100,title:"柜员号"}
            ,{field:'quota_name', width:160,title:"指标"}
            ,{field:'plan', width:120,title:"计划",edit:true}
            ,{field:'complete', width:120,title:"完成",edit:true}
            ,{field:'score', width:100,title:"得分"}
            ,{field:'add_time', width:180,title:"添加时间"}

             ,{field:'right', width:100 , title:"可选操作", toolbar: '#barDemo'}
        ]]
        ,id: 'bankuploaddetailtable'
    });





    //监听表格复选框选择
    // table.on('checkbox(performancemanagedemo)', function(obj) {
    //     console.log(obj)
    // });
    // table.on('edit(performancemanagedemo)', function(obj){
    //
    //         var value = obj.value //得到修改后的
    //         ,data = obj.data //得到所在行所有键值
    //         ,field = obj.field;//得到字段
    //     layer.msg('[ID: '+ data.ID +'] ' + field + '字段更改为:'+ value);
    //
    // });
    //监听工具条
    table.on('tool(bankuploadrecorddemo)', function(obj){
        var data = obj.data;
        console.log(data);
        if(obj.event === 'detail'){
            if (data.state != 4) {
                layui.jquery.ajax({
                    url: 'https://dqrcbankservice.com:8001/api/bankuploadrecord/' + data.id + "/",
                    type: 'PATCH',
                    contentType: 'application/json;charset=utf-8',
                    data: JSON.stringify({
                        state: 2
                    }),
                    error: function (res) {
                        if (res.status != 403) {
                            layer.alert('错误')
                        } else {
                            layer.alert('无权限操作此数据')
                        }
                    },
                    success: function (res) {
                        layer.msg('成功提交审核！')
                    },
                    beforeSend: function (xhr) {
                        token = window.localStorage.getItem('token');
                        xhr.setRequestHeader("authorization", "JWT " + token);
                    }
                });
            }else{
                layer.msg('已经审核通过！')
            }
        }else{
            console.log("other func");
        }
    });

    table.on('tool(bankuploaddetaildemo)', function(obj){
        var data = obj.data;
        // console.log(data,obj);
        if(obj.event === 'detail'){
            layui.jquery.ajax({
                url: 'https://dqrcbankservice.com:8001/api/bankuploadrecorddetail/' + data.id + "/",
                type: 'PATCH',
                contentType: 'application/json;charset=utf-8',
                data: JSON.stringify({
                    plan: data.plan,
                    complete:data.complete
                }),
                error: function (res) {
                    if (res.status != 403) {
                        layer.alert('错误')
                    } else {
                        layer.alert('无权限操作此数据')
                    }
                },
                success: function (res) {
                    layer.msg('信息修改成功！')
                },
                beforeSend: function (xhr) {
                    token = window.localStorage.getItem('token');
                    xhr.setRequestHeader("authorization", "JWT " + token);
                }
            });

        }else if(obj.event === 'delrecord') {
            layui.jquery.ajax({
                url: 'https://dqrcbankservice.com:8001/api/bankuploadrecorddetail/' + data.id + "/",
                type: 'DELETE',
                contentType: 'application/json;charset=utf-8',
                error: function (res) {
                    if (res.status != 403) {
                        layer.alert('错误')
                    } else {
                        layer.alert('无权限操作此数据')
                    }
                },
                success: function (res) {
                    layer.msg('成功删除');
                    obj.del();
                },
                beforeSend: function (xhr) {
                    token = window.localStorage.getItem('token');
                    xhr.setRequestHeader("authorization", "JWT " + token);
                }
            });
        }
    });


    var $ = layui.$, active = {
        getCheckData: function(obj,index){ //获取选中数据
            var checkStatus = table.checkStatus('performancemanage')
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
                table.reload('performancemanage');
            });

        }
        ,getCheckLength: function(){ //获取选中数目
            var checkStatus = table.checkStatus('performancemanage')
                ,data = checkStatus.data;
            layer.msg('选中了：'+ data.length + ' 个');
        }
        ,isAll: function(){ //验证是否全选
            var checkStatus = table.checkStatus('performancemanage');
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
    table.on('tool(performancemanagedemo)', function(obj){ //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
        var data = obj.data; //获得当前行数据
        //console.log(typeof(data))
        datajsonstr = JSON.stringify(data);
        WeAdminEdit('编辑','./edit.html',datajsonstr)
  })
}

function Delsrecord() {
    var table = layui.table;
    table.on('tool(performancemanagedemo)', function(obj){ //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
        var data = obj.data; //获得当前行数据
        console.log(obj)
        //datajsonstr = JSON.stringify(data);
         layui.jquery.ajax(
            {
                url: 'https://dqrcbankservice.com:8001/api/performancerecord/'+data.id,
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
        var info = layui.jquery("#info").val();
        var splitmethod = layui.jquery("#splitmethod").val();
        // console.log(srecdbackupinfo);
        //datajsonstr = JSON.stringify(data);
         layui.jquery.ajax(
            {
                url: 'https://dqrcbankservice.com:8001/api/performancerecord/',
                type: 'POST',
                contentType: 'application/json;charset=utf-8',
                data: JSON.stringify({
                        info:info,
                        splitmethod:splitmethod,
                    }),
                error: function (rest) {
                    if (res.status != 403){
                        layer.alert('未知错误！检查数据格式、字段名称')
                         }else{
                        layer.alert('无权限操作此数据')
                     }
                },
                success: function (rest) {

                    layer.alert("成功增加记录！");
                        var table = layui.table;
                        table.reload('testReload',{
                        url:'https://dqrcbankservice.com:8001/api/performancerecord/'
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
