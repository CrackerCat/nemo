$(function(){
    $("#org_add").click(function(){
        const org_name = $("#org_name").val();
        const org_status = $("#org_status").val();
        if(!org_name || !org_status){
            swal('Warning', '机构名称和机构状态不能为空', 'error');
        }else{
        $.post("/org-add",
        {
            "org_name": org_name,
            'status':org_status
        },function(data,e){
            if(e === "success"){
                swal({
                    title: "添加机构成功",
                    text: "",
                    type:"success",
                    confirmButtonText: "ok",
                    confirmButtonColor: "#41b883",
                    closeOnConfirm: false
                },
                function(){
                    location.href = "/org-add"
                });
            }else{
                swal('Warning', "添加机构失败!", 'error');
            }
        });}
    });

});