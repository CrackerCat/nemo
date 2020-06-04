$(function(){
    const org_name_selector = $("#org_name").bootstrapDualListbox({
        nonSelectedListLabel: '可选对象机构',
        selectedListLabel: '已选对象机构',
        filterTextClear: '清空过滤条件',
        filterPlaceHolder: '过滤条件',
        preserveSelectionOnMove: 'moved',
        moveOnSelect: false,
        infoText: '当前共 {0} 个机构',
        infoTextFiltered: '从 {1} 项 筛选 {0} 项',
        infoTextEmpty: 'Empty list',
        nonSelectedFilter: ''});

    const task_type_selector = $("#task_type").select2({
        //placeholder: '请选择任务类型',
        tags: true,
        maximumSelectionLength: 3  //最多能够选择的个数
        });
    
    
    $('#task_add').click(function(){
            const task_name = $("#task_name").val();
            const task_type = task_type_selector.val();
            const task_plan = $("#task_plan").val();
            const task_creator = $("#task_creator").val();
            const org_names = org_name_selector.val();

            org_name_selector.bootstrapDualListbox('refresh');
            if(!String(org_names)||!task_name||!task_type)
            {
                swal('warning', '标有星号的项均不能为空', 'error');
           }else{
            
               //org_name_obj.bootstrapDualListbox('destroy');
               $.post('/task-add',
               {'task_name': task_name,
                'task_type': String(task_type),
                'task_plan': task_plan,
                'org_names': String(org_names),
                'task_creator': task_creator
               },function(data, e){
                   if(e === 'success'){
                        swal('success', '任务添加成功', '');
                   }else{
                       swal('warning', '添加任务失败', 'error');
                   }
               }//post_callback_function
               );//post
           }
        });//onclick
});
