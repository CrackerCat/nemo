var language = {
    "sProcessing":   "处理中...",
    "buttons.copy":   "复制",
    "buttons.print":   "打印",
    "sLengthMenu":   "显示 _MENU_ 项结果。",
    "sZeroRecords":  "没有匹配结果",
    //"sInfo":         "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
    //"sInfoEmpty":    "显示第 0 至 0 项结果，共 0 项",
    //"sInfoFiltered": "(由 _MAX_ 项结果过滤)",
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
$('#domain_table').DataTable(
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
 "ajax": {
       "url": "/domain-list",
       "type": "post"
 },   
 columns:[
   {data: "index", title: "序号"},
   {data: "domain", title: "域名地址",
    render: function(data, type, full, meta){
        return '<a href="/details?domain=' + data + '">' + data + '</a>'
    }},
   {data: "ip", title: "IP地址"},
   {data: "title", title: "网站标题"},
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
