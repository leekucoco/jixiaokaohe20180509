layui.use('upload', function() {
    var $ = layui.jquery
        ,upload = layui.upload;
    //拖拽上传

    //layer.alert(token);
    upload.render({
        elem: '#test10'
        ,method:'post'
        // ,headers: {
        //     Authorization:token
        // } //可选项。额外的参数，如：{id: 123, abc: 'xxx'}
        ,url: '/uploadbasefile/'
        ,accept: 'file' //普通文件
        // ,exts: 'xlsx|doc|xls' //只允许上传压缩文件
        , done: function (res) {
            console.log(res)
            //layer.alert(res.success)
        },
                     //        beforeSend: function(xhr) {
                     //    token = window.localStorage.getItem('token');
                     //     xhr.setRequestHeader("authorization", "JWT " + token);
                     // }
    });
    //多文件列表示例

        var demoListView = $('#demoList');
        var token = localStorage.getItem("token");
          //var csrftoken = $.cookie('csrftoken');
        token = "JWT "+token;
        selecter = "#recordsid";
        var recordid = 0;
        if($(selecter).val() != ""){
           recordid = $(selecter).val();
        }else {
            recordid = 0
        }

        uploadListIns = upload.render({
                elem: '#testList'
                ,url: '/salaryrecord/'+recordid+'/'
                ,method:'patch'
                ,headers: {
                    "Authorization":token
                } //可选项。额外的参数，如：{id: 123, abc: 'xxx'}
                //headers为自己修改的项目。在lay/upload.js文件 先修改p.prototype.config增加headers="",然后修改ajax
                //增加headers:l.headers其他需要验证的组件依次方法修改
                ,data:{
                    status: "CHECKONWORKATTENDANCECOMPLETE",
                }
                ,field:'checkonworkfile'
                ,accept: 'file'
                //,exts: 'xlsx|doc|xls' //只允许上传压缩文件
                ,multiple: true
                ,auto: false
                ,bindAction: '#testListAction'
                // ,before: function (xhr) {
                //             token = window.localStorage.getItem('token');
                //             xhr.setRequestHeader("authorization", "JWT " + token);
                //         }
                ,choose: function(obj){
                    var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
                    //读取本地文件
                   //console.log(files["0"])
                   //  for (i in files){
                   //      console.log(uploadListIns)
                   //     // uploadListIns.config.data.filename = files[i].name
                   //  }


                    obj.preview(function(index, file, result){
                        //uploadListIns.config.data.filename = file.name
                        //console.log(uploadListIns)
                        //console.log(upload)
                        var tr = $(['<tr id="upload-'+ index +'">'
                            ,'<td>'+ file.name +'</td>'
                            ,'<td>'+ (file.size/1014).toFixed(1) +'kb</td>'
                            ,'<td>等待上传</td>'
                            ,'<td>'
                            ,'<a class="layui-btn layui-btn-mini demo-reload layui-hide">重传</a>'
                            ,'<a class="layui-btn layui-btn-mini layui-btn-danger demo-delete">删除</a>'
                            ,'</td>'
                            ,'</tr>'].join(''));

                        //单个重传
                        tr.find('.demo-reload').on('click', function(){
                            obj.upload(index, file);
                        });

                        //删除
                        tr.find('.demo-delete').on('click', function(){
                            delete files[index]; //删除对应的文件
                            tr.remove();
                            uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
                        });

                        demoListView.append(tr);
                    });
                }
                // ,before:function (obj) {
                //     console.log(obj)
                // }
                ,done: function(res, index, upload){
                    if(res){ //上传成功
                        var tr = demoListView.find('tr#upload-'+ index)
                            ,tds = tr.children();
                        tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
                        tds.eq(3).html('<button class="layui-btn layui-btn-mini demo-init" >生成数据</button>'); //清空操作
                        tds.eq(3).find('.demo-init').on('click',function(){
                            //console.log("clicked")
                            //layer.alert(tds.eq(0).text())
                            layui.jquery.ajax(
                                {
                                    url: '/api/v1/getonestaffrecord',
                                    type: 'GET',
                                    contentType: 'application/json;charset=utf-8',

                                    data: {filename:tds.eq(0).text()},
                                    error : function () {
                                        layer.alert("系统出现故障，生成数据失败");
                                    },
                                    success : function () {
                                        //obj.del();
                                        //layer.alert(res);
                                        //console.log(res)
                                        layer.alert("成功发送数据库初始化请求，等待响应结果");
                                    }
                                }
                            );

                        });


                        return delete this.files[index]; //删除文件队列已经上传成功的文件

                    }

                    this.error(index, upload);

                }
                ,error: function(index, upload){
                    var tr = demoListView.find('tr#upload-'+ index)
                        ,tds = tr.children();
                    tds.eq(2).html('<span style="color: #ff5722;">上传失败</span>');
                    tds.eq(3).find('.demo-reload').removeClass('layui-hide'); //显示重传
                }
    });
});
