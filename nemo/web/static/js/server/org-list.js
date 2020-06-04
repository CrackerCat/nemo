var language = {//语言设置
    //"sUrl": "/ip-asset-list",
       sProcessing: "处理中...",
       sZeroRecords: "没有匹配结果",
       sLenthMenu: "每页显示 _MENU_ 条记录",
       sInfo: "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
       sInfoEmpty: "没有数据",
       sInfoFiltered: "(获取 _MAX_ 项结果)",
       sInfoPostFix: "",
       sSearch: "搜索:",
       sUrl: "",
       sEmptyTable: "表中数据为空",
       sLoadingRecords: "载入中...",
       sInfoThousands: ",",
       oPaginate: {
         sFirst: "首页",
         sPrevious: "上页",
         sNext: "下页",
         sLast: "末页"
        }
 };
$(document).ready(function(){
$('#ip_asset_table').DataTable(
{
 "rowID":'uuid',
 "paging": true,
 "searching": false,
 "processing": true,
 "serverSide": true,
 "autowidth": false,
 "sort": false,
 "language": language,
 "ajax": {
       "url": "/org-list",
       "type": "post"
 },   
 
 columns:[
   {data: "id", 
     title: '<input title="checkbox_all" type="checkbox" id="all_select" value="1" />', 
     "sClass" : "center",
     "salign" : "center",
     "render": function(data, type, full){return '<input title="checkbox_all" type="checkbox" id="select_id" value="1"/>';}
   },
   {data: "index", title: "序号"},
   {data: "org_name", title: "机构名称"},
   {data: "status", title: "状态"},
   {data: "sort_order", title: "机构ID"},
   {data: "create_time", title: "创建时间"},
   {data: "update_time", title: "更新时间"},
   {title: "操作",
     data: null,
     "render": function (data, type, full, meta) {
         var strModify = "<a href='/org-modify'><i class='fa fa-pencil'></i><span>修改</span></a>&nbsp;&nbsp;";
         var strDelete = "<a href='/org-delete'><i class='fa fa-pencil'></i><span>删除</span></a>";
         return strModify + strDelete;
     }
   }
 ]
}

);//end datatable
});

