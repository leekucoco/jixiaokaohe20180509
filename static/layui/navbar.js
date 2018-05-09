layui.use(['element','layer','laytpl'], function(){
    var element = layui.element; //导航的hover效果、二级菜单等功能，需要依赖element模块
    var laytpl = layui.laytpl;

    // var data = { //数据
    //     "title":"Layui常用模块"
    //     ,"list":[{"modname":"弹层","alias":"layer","site":"layer.layui.com"},{"modname":"表单","alias":"form"}]
    // };
    //
    // var ht =
    //   "<h3>{{ d.title }} </h3><ul>"+
    //    " {{#  layui.each(d.list, function(index, item){ }}"+
    //     "<li>"+
    //       "<span>{{ item.modname }} </span>"+
    //       "<span>{{ item.alias }}：</span>"+
    //       "<span>{{ item.site || '' }}</span>"+
    //     "</li>"+
    //     "{{#  }); }}"+
    //     "{{#  if(d.list.length === 0){ }}"+ "无数据" +
    //         "{{#  } }}"+
    //   "</ul>"
    // var getTpl = ht
    //     // console.log(getTpl)
    // ,view = document.getElementById('view');
    //     // console.log(view);
    // laytpl(getTpl).render(data, function(html){
    //     view.innerHTML = html;
    // });

    //监听导航点击
    element.on('nav(leftbar)', function(elem){
        console.log(elem);
        //layer.msg(elem.text());
        if (elem.text() == "全行员工系数明细"){
            //layui.jquery("#allbody").empty();

            layui.jquery("#allbody").html(
            '<div style="padding: 15px;">系数明细管理页面</div>'+
                 '<div class="layui-row">'+
                    '<div class="layui-col-md4">'+
                        // '<div class="layui-btn-group demoTable">'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="getCheckData" lay-event="mutidel">删除选中行数据</button>'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="getCheckLength">获取选中数目</button>'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="isAll">验证是否全选</button>'+
                        // '</div>'+
                    '</div>'+
                    '<div class="layui-col-md4 layui-col-md-offset1">'+
                        // '<div class="grid-demo">' +
               ' <form class="layui-form layui-form-pane" action="">'+

              '<div class="layui-form-item">'+

                '<div class="layui-input-inline">'+
                  '<input name="title" lay-verify="title" id = "coefficientname" autocomplete="off" placeholder="请输入姓名" class="layui-input" type="text">'+
             ' </div>'+
                // '<label class="layui-form-label">搜索</label>'+  searchcoefficientbyname();return false;
                '<button class="layui-btn layui-btn-primary" onclick="searchcoefficientbyname();return false;"><i class="layui-icon">&#xe615;</i></button>'+
                // '<button class="layui-btn layui-btn-primary" data-type="reload" ><i class="layui-icon">&#xe615;</i></button>'+
                '</div>'+
                '</form>'+

                 '</div>'+
                    '</div>'+
                '</div>'+
                '<table class="layui-hide" id="idTest" lay-filter="demo"></table>'+
                '<script type="text/html" id="barDemo">'+
                '<a class="layui-btn layui-btn-primary layui-btn-sm" lay-event="detail">查看</a>'+
                // '<a class="layui-btn layui-btn-sm" lay-event="update">更新</a>'+
                // '<a class="layui-btn layui-btn-danger layui-btn-sm" lay-event="del">删除</a>'+
                '</script>'+
                '<script src="/static/layui/tablerender.js"></script>'
                
        );

        }
        if (elem.text() == "数据上传"){

            layui.jquery("#allbody").empty();

            layui.jquery("#allbody").html(
                '<script src="/static/layui/uploadfile.js"></script>'+
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

        if (elem.text() == "发起绩效考核"){
            layui.jquery("#allbody").empty();
            layui.jquery("#allbody").html(
             '<div style="padding: 15px;">生成本月工资记录</div>'+
                 '<div class="layui-row">'+
                    '<div class="layui-col-md4">'+
                        // '<div class="layui-btn-group demoTable">'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="getCheckData" lay-event="mutidel">删除选中行数据</button>'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="getCheckLength">获取选中数目</button>'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="isAll">验证是否全选</button>'+
                        // '</div>'+
                    '</div>'+
                    '<div class="layui-col-md4 layui-col-md-offset1">'+
                        // '<div class="grid-demo">' +
                    '</div>'+
                 '</div>'+
                 '<form class="layui-form">'+
                      '<div class="layui-form-item ">'+
                        '<label class="layui-form-label">工资记录</label>'+
                        '<div class="layui-input-inline">'+
                            '<input type="hidden" name="status" value="UNCOMPELTE" >'+
                            '<input type="text" name="extrainfo" lay-verify="title" autocomplete="off" placeholder="工资记录名称（默认为空）" class="layui-input">'+
                        '</div>'+
                      '</div>'+
                      '<div class="layui-form-item">'+

                        '<div class="layui-input-block">'+
                               '<button class="layui-btn"  lay-submit lay-filter="formsubmit">立即提交</button>'+
                                '<button type="reset" class="layui-btn layui-btn-primary">重置</button>'+
                        '</div>'+
                        '</div>'+
                  '</form>'+
                     '<table class="layui-hide" id="fqjxkh" lay-filter="fqjxkhfilter"></table>'+
                '<script type="text/html" id="barDemo">'+
                '<a class="layui-btn layui-btn-primary layui-btn-sm" lay-event="detail">查看</a>'+
                //'<a class="layui-btn layui-btn-sm" lay-event="update">更新</a>'+
                '<a class="layui-btn layui-btn-danger layui-btn-sm" lay-event="del">删除</a>'+
                '</script>'+
                '<script src="/static/layui/fqjxkh.js"></script>'+
                    '<script>'+
                    'layui.use("form", function(){' +
                      'var form = layui.form;'+
                      'form.on("submit(formsubmit)", function(data){'+
                        //'layer.msg(JSON.stringify(data.field));'+
                            //'console.log(data);'+
                           ' if (data.field.extrainfo == ""){ data.field.extrainfo = undefined}'+
                         'layui.jquery.ajax({'+
                                'url: "https://dqrcbankservice.com:8001/salaryrecord/",'+
                                'type: "POST",'+
                                'contentType: "application/json;charset=utf-8",'+
                                'data: JSON.stringify(data.field),'+
                                'error : function (res) {'+
                                    'if (res.status != 403){'+
                                    'layer.alert("未知的错")'+
                                     '}else{'+
                                    'layer.alert("无权限操作此数据")'+
                                 '}'+
                                '},'+
                                'success : function (res) {'+
                                    'layer.msg("成功生成工资记录");'+
                                '},'+
                                'beforeSend: function(xhr) {'+
                                    'token = window.localStorage.getItem("token");'+
                                    'xhr.setRequestHeader("authorization", "JWT " + token);'+
                             '}});'+
                            'return false;'+
                      '});'+
                    '});'+
                    '</script>'

            );

        }


        if (elem.text() == "录入考勤信息"){
            layui.jquery("#allbody").empty();
            layui.jquery("#allbody").html(
             '<div style="padding: 15px;">录入考勤信息</div>'+
                 '<div class="layui-row">'+
                    '<div class="layui-col-md4">'+
                        // '<div class="layui-btn-group demoTable">'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="getCheckData" lay-event="mutidel">删除选中行数据</button>'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="getCheckLength">获取选中数目</button>'+
                        //     '<button class="layui-btn layui-btn-sm" data-type="isAll">验证是否全选</button>'+
                        // '</div>'+
                    '</div>'+
                    '<div class="layui-col-md4 layui-col-md-offset1">'+
                        // '<div class="grid-demo">' +
                    '</div>'+
                 '</div>'+
                 // '<form class="layui-form">'+
                 //      '<div class="layui-form-item ">'+
                 //        '<label class="layui-form-label">工资记录</label>'+
                 //        '<div class="layui-input-inline">'+
                 //            '<input type="hidden" name="status" value="UNCOMPELTE" >'+
                 //            '<input type="text" name="extrainfo" lay-verify="title" autocomplete="off" placeholder="工资记录名称（默认为空）" class="layui-input">'+
                 //        '</div>'+
                 //      '</div>'+
                 //      '<div class="layui-form-item">'+
                 //
                 //        '<div class="layui-input-block">'+
                 //               '<button class="layui-btn"  lay-submit lay-filter="formsubmit">立即提交</button>'+
                 //                '<button type="reset" class="layui-btn layui-btn-primary">重置</button>'+
                 //        '</div>'+
                 //        '</div>'+
                 //  '</form>'+
                     '<table class="layui-hide" id="fqjxkh" lay-filter="fqjxkhfilter"></table>'+
                '<script type="text/html" id="barDemo">'+
                '<a class="layui-btn layui-btn-primary layui-btn-sm" lay-event="detail">查看</a>'+
                //'<a class="layui-btn layui-btn-sm" lay-event="update">更新</a>'+
                '<a class="layui-btn layui-btn-normal layui-btn-sm" lay-event="update" id = "kqsq">上传</a>'+
                '</script>'+
                  // '<div class="layui-upload">'+

                // '</div>'+
                '<div id = "kqluru"></div>'+
                '<script src="/static/layui/fqjxkh.js"></script>'+
                    '<script>'+
                    'layui.use("form", function(){' +
                      'var form = layui.form;'+
                      'form.on("submit(formsubmit)", function(data){'+
                        //'layer.msg(JSON.stringify(data.field));'+
                            //'console.log(data);'+
                           ' if (data.field.extrainfo == ""){ data.field.extrainfo = undefined}'+
                         'layui.jquery.ajax({'+
                                'url: "https://dqrcbankservice.com:8001/salaryrecord/",'+
                                'type: "POST",'+
                                'contentType: "application/json;charset=utf-8",'+
                                'data: JSON.stringify(data.field),'+
                                'error : function (res) {'+
                                    'if (res.status != 403){'+
                                    'layer.alert("未知的错")'+
                                     '}else{'+
                                    'layer.alert("无权限操作此数据")'+
                                 '}'+
                                '},'+
                                'success : function (res) {'+
                                    'layer.msg("成功");'+
                                '},'+
                                'beforeSend: function(xhr) {'+
                                    'token = window.localStorage.getItem("token");'+
                                    'xhr.setRequestHeader("authorization", "JWT " + token);'+
                             '}});'+
                            'return false;'+
                      '});'+
                    '});'+
                    '</script>'

            );

        }

    });
});

