
layui.use(['form','upload'], function () {
    var $ = layui.jquery
        , upload = layui.upload
        ,form = layui.form;
    // //拖拽上传
    var token = localStorage.getItem("token");
    token = "JWT " + token;
    // //layer.alert(token);
    // upload.render({
    //     elem: '#test10'
    //     , method: 'post'
    //     , headers: {
    //         Authorization: token
    //     } //可选项。额外的参数，如：{id: 123, abc: 'xxx'}
    //     , url: '/uploadbasefile/'
    //     , accept: 'file' //普通文件
    //     // ,exts: 'xlsx|doc|xls' //只允许上传压缩文件
    //     , done: function (res) {
    //         console.log(res)
    //         //layer.alert(res.success)
    //     }
    // });
    //多文件列表示例


    var demoListView = $('#demoList')

        , uploadListIns = upload.render({

        elem: '#testList'
        , url: ""
        , method: 'patch'
        , headers: {
            Authorization: token,
            ContentType: "application/x-www-form-urlencoded",
        } //可选项。额外的参数，如：{id: 123, abc: 'xxx'}
        //headers为自己修改的项目。在lay/upload.js文件 先修改p.prototype.config增加headers="",然后修改ajax
        //增加headers:l.headers其他需要验证的组件依次方法修改
        , data: {
            status: ""
        }
        , field: ""
        , accept: 'file'
        , exts: 'xlsx|doc|xls' //只允许上传压缩文件
        , multiple: true
        , auto: false
        , bindAction: '#testListAction'

        , choose: function (obj) {

            var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
            //读取本地文件
            //console.log(files[0])
            //  for (i in files){
            //      console.log(uploadListIns)
            //     // uploadListIns.config.data.filename = files[i].name
            //  }


            obj.preview(function (index, file, result) {


                //console.log(file)
                //uploadListIns.config.data.filename = file.name
                //console.log(uploadListIns)
                //console.log(upload)
                var tr = $(['<tr id="upload-' + index + '">'
                    , '<td>' + file.name + '</td>'
                    , '<td>' + (file.size / 1014).toFixed(1) + 'kb</td>'
                    , '<td>等待上传</td>'
                    , '<td>'
                    , '<a class="layui-btn layui-btn-mini demo-reload layui-hide">重传</a>'
                    , '<a class="layui-btn layui-btn-mini layui-btn-danger demo-delete">删除</a>'
                    , '</td>'
                    , '</tr>'].join(''));

                //单个重传
                tr.find('.demo-reload').on('click', function () {
                    obj.upload(index, file);
                });

                //删除
                tr.find('.demo-delete').on('click', function () {
                    delete files[index]; //删除对应的文件
                    tr.remove();
                    uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
                });

                demoListView.append(tr);
            });
        }

        ,before:function (obj) {
                var tmpdata = $('input[name="dataId"]').val();
                var jsobj = JSON.parse(tmpdata);

                //console.log("upload" + tmpdata)
                status = $('input[name="salaryfileinfo"]').val();
                //console.log(stype)
                jsobjid = jsobj.id


                url =  'https://dqrcbankservice.com:8001/api/salaryrecord/' + jsobjid + '/'
                if(status == "CHECKONWORKATTENDANCECOMPLETE"){
                    field = "checkonworkfile"
                }else if(status == "TOTALSALARYCOMPLETE"){
                    field = "baseandwelfareaddfile"
                }else if(status == "INSURANCEANDFUNDCOMPELTE"){
                    field = "insuranceandfundfile"
                }else if(status == "TAXANDOTHERDEDUCTIONS"){
                    field = "taxandotherdeductionfile"
                }
                uploadListIns.config.url = url
                uploadListIns.config.field = field
                uploadListIns.config.data.status = status

                console.log(uploadListIns)
        }
        , done: function ( res, index, upload) {
           // var files = this.files = obj.pushFile();
            console.log(this.files[index])
            if (res) { //上传成功
          //       layer.alert("上传成功", {icon: 6},function () {
          //                        // 获得frame索引
          //   var index = parent.layer.getFrameIndex(window.name);
          //    //关闭当前frame
          //   parent.layer.close(index);
          // });
                //console.log(res)
                var wb;//读取完成的数据
                var rABS = false; //是否将文件读取为二进制字符串
                var f = this.files[index];
                var reader = new FileReader();
                reader.onload = function(e) {
                    var data = e.target.result;
                    if(rABS) {
                        wb = XLSX.read(btoa(fixdata(data)), {//手动转化
                            type: 'base64'
                        });
                    } else {
                        wb = XLSX.read(data, {
                            type: 'binary'
                        });
                    }

                    //wb.SheetNames[0]是获取Sheets中第一个Sheet的名字
                    //wb.Sheets[Sheet名]获取第一个Sheet的数据
                    //document.getElementById("demo").innerHTML= JSON.stringify( XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]) );
                };
                if(rABS) {
                    reader.readAsArrayBuffer(f);
                } else {
                    reader.readAsBinaryString(f);
                }


            function fixdata(data) { //文件流转BinaryString
                var o = "",
                    l = 0,
                    w = 10240;
                for(; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)));
                o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)));
                return o;
            }


                var tr = demoListView.find('tr#upload-' + index)
                    , tds = tr.children();
                tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
                tds.eq(3).html('<button class="layui-btn layui-btn-mini demo-init" >生成数据</button>'); //清空操作
                tds.eq(3).find('.demo-init').on('click', function () {
                   var toserjson =  XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]])
                    console.log(toserjson)
                    // for(var i=0;i<toserjson.length;i++) {
                    //     srecordid = res.id
                    //     //console.log(srecordid)
                    //     username = toserjson[i]["id"]
                    //     //console.log(toserjson[i]["id"]);
                    status = $('input[name="salaryfileinfo"]').val();
                    var datatosend = {}
                    datatosend["id"] = res.id
                    datatosend["status"] = status
                    datatosend["jsonobj"] = toserjson
                        layui.jquery.ajax(
                            {
                                url: 'https://dqrcbankservice.com:8001/api/fsalaryrecorddata/',
                                type: 'POST',
                                contentType: 'application/json;charset=utf-8',
                                data: JSON.stringify(datatosend),
                                error: function (rest) {
                                    if (res.status != 403){
                                        layer.alert('未知错误！检查数据格式、字段名称')
                                         }else{
                                        layer.alert('无权限操作此数据')
                                     }
                                },
                                success: function (rest) {
                                    //obj.del();
                                    var resjson = JSON.parse(rest)
                                    successcount = resjson.successcount
                                    if (resjson.faildata != "") {
                                        faildata = resjson.faildata
                                        alertstr = "上传成功"+successcount+"条数据"+"\n"+"失败用户："+faildata
                                    }else{
                                         // faildata = resjson.faildata
                                        alertstr = "上传成功"+successcount+"条数据"
                                    }
                                    layer.alert(alertstr, {icon: 6},function () {
                                        var index = parent.layer.getFrameIndex(window.name);
                                         //关闭当前frame
                                        parent.layer.close(index);
                                      });

                                    //layer.alert("成功发送数据库初始化请求，等待响应结果");
                                },
                               beforeSend: function(xhr) {
                                    token = window.localStorage.getItem('token');
                                    xhr.setRequestHeader("authorization", "JWT " + token);
                                }
                            }
                        );
                    // }
                });

                return delete this.files[index]; //删除文件队列已经上传成功的文件
            }

            this.error(index, upload);

        }
        , error: function (index, upload) {
            var tr = demoListView.find('tr#upload-' + index)
                , tds = tr.children();
            tds.eq(2).html('<span style="color: #ff5722;">上传失败</span>');
            tds.eq(3).find('.demo-reload').removeClass('layui-hide'); //显示重传
        }
    });
});

