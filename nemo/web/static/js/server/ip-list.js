$("#search").click(function(){
    const org_name = $("#org_name").val();
    const ip_addr = $("#ip_address").val();
    const port = $("#port").val();
    $.post('/ip-list',
        {
            "org_name": org_name,
            "ip_addr": ip_addr,
            "port": port
        },
        function(data, e, meta){
            if(e === "success"){
                const search_data = data;
                swal("success", "搜索数据成功", "Done");
            }else{
                swal("error", "没有搜索到数据", 'Failed');
            }
        }
    );

});

var language = {
    "sProcessing":   "处理中...",
    "buttons.copy":   "复制",
    "buttons.print":   "打印",
    "sLengthMenu":   "显示 _MENU_ 项结果。",
    "sZeroRecords":  "没有匹配结果",
    "sInfo":         "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
    "sInfoEmpty":    "显示第 0 至 0 项结果，共 0 项",
    "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
    "sInfoPostFix":  "",
    "sSearch":       "搜索:",
    "sUrl":          "",
    "sEmptyTable":     "表中数据为空",
    "sLoadingRecords": "载入中...",
    "sInfoThousands":  ",",
    "oPaginate": {
        "sFirst":    "首页",
        "sPrevious": "上页",
        "sNext":     "下页",
        "sLast":     "末页"
    },
    "oAria": {
        "sSortAscending":  ": 以升序排列此列",
        "sSortDescending": ": 以降序排列此列"
    }
};

$(document).ready(function(){
    
$('#ip_table').DataTable(
{
 "paging": true,
 "searching": false,
 "processing": true,
 "serverSide": true,
 "autowidth": false,
 "sort": false,
 "bLengthChange":true,
 "pagingType":"full_numbers",//分页样式
 "language": language,
 searchable:false,//搜索总开关
 searching:false,
 ordering:true,//排序总开关
 destroy:true,
 dom: '<t><lfip>',
 //data: search_data,
 
 "ajax": {
       "url": "/ip-list",
       "type": "post"
 },
 columns:[
    /*
   {data: "id", 
     title: '<input title="checkbox_all" type="checkbox" id="all_select" value="1" />', 
     "sClass" : "center",
     "salign" : "center",
     "render": function(data, type, full){return '<input title="checkbox_all" type="checkbox" id="all_select" value="1"/>';}
   },*/
   {data: "index", title: "序号"},
   {data: "ip", title: "IP地址", 
   render:function(data, type, full, meta){
        return '<a href="/details/?ip=' + data + '">' + data + '</a>';
   }},
   {data: "port", title: "端口"},
   {data: "org_name", title: "所属组织"},
   {data: "update_time", title: "更新时间"},
   {title: "操作",
     data: null,
     "render": function (data, type, full, meta) {
         var strModify = "<a href='/ip-modify'><i class='fa fa-pencil'></i><span>修改</span></a>&nbsp;&nbsp;";
         var strDelete = "<a href='/ip-delete'><i class='fa fa-pencil'></i><span>删除</span></a>";
         return strModify + strDelete;
     }
   }
 ],
 infoCallback:function(settings,start,end,max,total,pre) {
    var api = this.api();
    var pageInfo = api.page.info();
    return "共"+pageInfo.pages +"页,当前显示"+ start + "到" + end + "条记录" + ",共有"+ total + "条记录";
},
}

);//end datatable
});


