layui.use('table', function(){
    var table = layui.table;
    //tables.set();
    token = window.localStorage.getItem('token');
    token =  "JWT " + token

    table.render({
        elem: '#fqjxkh'
        ,url:'/salaryrecord/'
        ,height: 'full-200'
        ,page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
            layout: ['limit', 'count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
            //,curr: 5 //设定初始在第 5 页
            ,groups: 3 //只显示 1 个连续页码
            ,first: false //不显示首页
            ,last: false//不显示尾页
        }
        // ,headers: {
        //     Authorization:token
        // } //可选项。额外的参数，如：{id: 123, abc: 'xxx'}
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
            //,{field:'id',  wide:80, sort: true, title:"id"}
            //,{field:'idcardnumber', width:180,title:"员工身份证号"}
            //,{field:'id',width:80, title:"id"}
            ,{field:'date',width:120,sort: true,title:"日期"}
             ,{field:'extrainfo',width:150, edit:true, title:"记录名称"}
             , {
                field: 'status', width: 400, title: "记录状态"
                , templet: function (d) {
                    //console.log(d)
                    var dict = new Array();
                    dict["UNCOMPELTE"] = "尚未完成本月工资核算";
                    dict["BASESALARYINITCOMPLETE"] = "已生成基础工资与福利薪酬";
                    dict["CHECKONWORKATTENDANCECOMPLETE"] = "完成考勤录入";
                    dict["TOTALSALARYCOMPLETE"] = "已生成薪酬合计";
                    dict["INSURANCEANDFUNDCOMPELTE"] = "已经录入五险一金并生成应发薪酬";
                    dict["TAXANDOTHERDEDUCTIONS"] = "已完成税费及其他扣除项录入生成实发薪酬";
                    return dict[d.status]
                }
            }
            ,{field:'right', width:200 , title:"", toolbar: '#barDemo'}
        ]]
        ,id: 'fqjxkhid'
    //     ,done: function (res) {
    //             console.log(res);
    //
    // }
    //         ,beforeSend: function(xhr) {
    //             token = window.localStorage.getItem('token');
    //             xhr.setRequestHeader("authorization", "JWT " + token);
    //         }
    });



    //监听表格复选框选择
    table.on('checkbox(fqjxkhfilter)', function(obj) {
        console.log(obj)
    });
    table.on('edit(fqjxkhfilter)', function(obj){

              var value = obj.value //得到修改后的
            ,data = obj.data //得到所在行所有键值
            ,field = obj.field;//得到字段
        layer.msg('[ID: '+ data.ID +'] ' + field + '字段更改为:'+ value);

    });
    //监听工具条
    table.on('tool(fqjxkhfilter)', function(obj){
        var data = obj.data;
        var msg = ""
        var html = '<div class="layui-form">'+
            '<table class="layui-table" id="certable">'+
            '<colgroup> <col width="150"> <col width="150"> <col width="300"> <col> </colgroup>'+
            '<thead> <tr> <th>生成日期</th> <th>修改日期</th> <th>记录状态</th></tr> </thead><tbody>'
        var dict = new Array();
        dict["UNCOMPELTE"] = "尚未完成本月工资核算";
        dict["BASESALARYINITCOMPLETE"] = "已生成基础工资与福利薪酬";
        dict["CHECKONWORKATTENDANCECOMPLETE"] = "完成考勤录入";
        dict["TOTALSALARYCOMPLETE"] = "已生成薪酬合计";
        dict["INSURANCEANDFUNDCOMPELTE"] = "已经录入五险一金并生成应发薪酬";
        dict["TAXANDOTHERDEDUCTIONS"] = "已完成税费及其他扣除项录入生成实发薪酬";
        if(obj.event === 'detail'){
            if(data.count!= 0){
                    html = html+"<tr> <td>"+data.add_time+
                        "</td> <td>"+data.update_time+
                        "</td> <td>" +dict[data.status] + "</td></tr>"
                   // msg = msg + data.certificates[i].certificate

            }else{
                html = html +"<tr> <td>信息不存在</td></tr>>"
            }
            //layer.msg('ID：'+ data.ID + ' 的查看操作'+data.certificates[0].certificate);

            layer.open({
                type: 1,
                title: '工资记录信息详情',
                shadeClose: true,
                shade: false,
                maxmin: true, //开启最大化最小化按钮
                area: ['800px', '300px'],
                content: html+'</tbody> </table> </div>'
            });
        } else if(obj.event === 'del'){
            console.log(obj.data)
            layer.confirm('是否删除此条记录并删除与其关联的全部工资数据', function(index){
                layui.jquery.ajax(
                    {
                        url: '/salaryrecord/'+obj.data.id,
                        type: 'DELETE',
                        contentType: 'application/json;charset=utf-8',
                        //data: JSON.stringify(data),
                        error : function (res) {
                            if (res.status != 403){
                            layer.alert('未知的错误')
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
            console.log(obj.data)

            layui.jquery("#kqluru").html(

                '<script src="/static/layui/uploadfile.js"></script>'+
                '<input type="hidden" name="re" id="recordsid" value='+obj.data.id+'>'+
                '<div class="layui-upload">'+
                '<button type="button" class="layui-btn layui-btn-normal" id="testList">选择多文件</button>'+
                '<div class="layui-upload-list">'+
                '<table class="layui-table">'+
                '<thead>'+
                '<tr><th>文件名</th>'+
                '<th>大小</th>'+
                '<th>状态</th>'+
                '<th>操作</th>'+
                '</tr></thead>'+
                '<tbody id="demoList"></tbody>'+
                '</table>'+
                '</div>'+
                '<button type="button" class="layui-btn" id="testListAction">开始上传</button>'+
                '</div>'
            );
        }
    });



    var $ = layui.$, active = {
    //     reload: function(){
    //       var demoReload = $('#coefficientname');
    //       //执行重载
    //       table.reload('testReload', {
    //         page: {
    //           curr: 1 //重新从第 1 页开始
    //         }
    //         ,where: {
    //           // key: {
    //             search: demoReload.val()
    //           // }
    //         }
    //       });
    // },
        getCheckData: function(obj,index){ //获取选中数据
            var checkStatus = table.checkStatus('idTest')
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
                table.reload('idTest');
            });

        }
        ,getCheckLength: function(){ //获取选中数目
            var checkStatus = table.checkStatus('idTest')
                ,data = checkStatus.data;
            layer.msg('选中了：'+ data.length + ' 个');
        }
        ,isAll: function(){ //验证是否全选
            var checkStatus = table.checkStatus('idTest');
            layer.msg(checkStatus.isAll ? '全选': '未全选')
        }
    };
    // $('.demoTable.layui-btn').on('click', function(){
    //     var type = $(this).data('type');
    //     active[type] ? active[type].call(this) : '';
    // });
    // $('.demoTable.layui-btn').on('click', function(){
    //     var type = $(this).data('type');
    //     active[type] ? active[type].call(this) : '';
    // });
});



function searchcoefficientbyname() {
    var data = layui.jquery("#coefficientname").val();
    //console.log(data);
    var table = layui.table;
    layui.use('table', function () {
        layui.jquery.ajax(
            {
                url: '/cofficient/?search=' + data,
                type: 'GET',
                contentType: 'application/json;charset=utf-8',
                // data: JSON.stringify({
                //     coefficent:parseFloat(obj.data.coefficent),
                //     user:parseInt(obj.data.user)
                // }),

                error: function (res) {
                    console.log(res);
                    if (res.status != 403) {
                        layer.alert('未知的错我')
                    } else {
                        layer.alert('无权限操作此数据')
                    }

                },

                success: function (res) {
                    //var data = layui.jquery.parseJSON(res)
                    layui.jquery("#idTest").empty();
                    // console.log(res);
                    // table.render({
                    data = res;

                    table.render({
                        elem: '#idTest'
                        ,data: data.results
                        // , even: true
                        ,page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
                            layout: ['limit', 'count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                            // ,elem: 'idTest'
                            ,count: data.count
                            ,curr: 1 //设定初始在第 5 页
                            ,limit:20
                            ,groups: 3 //只显示 1 个连续页码
                            ,first: false //不显示首页
                            ,last: false//不显示尾页
                        }
                        // ,response: {
                        //     statusName: 'status' //数据状态的字段名称，默认：code
                        //     ,statusCode: 200 //成功的状态码，默认：0
                        //     // ,msgName: 'hint' //状态信息的字段名称，默认：msg
                        //     ,countName: 'count' //数据总数的字段名称，默认：count
                        //     ,dataName: 'results' //数据列表的字段名称，默认：data
                        // }
                        , cols: [[
                            {type:'checkbox', fixed: 'left'}
                            //,{field:'id',  wide:80, sort: true, title:"id"}
                            //,{field:'idcardnumber', width:180,title:"员工身份证号"}
                            ,{field:'name',width:80, title:"姓名"}
                            ,{field:'depart',width:120,sort: true,title:"部门"
                                ,templet: function (d) {
                                    return d.depart.name
                                 }
                             }
                             ,{field:'coefficent',width:80, edit:true, title:"系数"}
                             ,{field:'joinedyears',width:120,  title:"参加工作时间"}
                             ,{field:'yearsofwork',width:100,  title:"工作年限"}
                             ,{field:'certificatetotalscore',width:120,  title:"证书得分"}
                             ,{field:'education',width:120,  title:"学历"
                                ,templet: function (d) {
                                    //console.log(d)
                                    educations = ["高中（中专）及以下","大学专科","大学本科","硕士研究生","博士研究生及以上"]
                                    return educations[d.education-1]
                                 }
                             }
                             ,{field:'rank13',width:100,  title:"行员等级"}
                             ,{field:'post',width:120,  title:"岗位"}
                            ,{field:'right', width:100 , title:"证书明细", toolbar: '#barDemo'}
                        ]]

                    });
                    //console.log(data)

                },
                beforeSend: function (xhr) {
                    token = window.localStorage.getItem('token');
                    xhr.setRequestHeader("authorization", "JWT " + token);
                }
            }
        );

    });

}