/**
 * 二级菜单中加入数字显示
 * 函数模板：
 * function 列表的权限标识(id){
 * 
 * 	$("#"+id).text("(数值)");
 * }
 */
var head_menu_array = {
    convertUnderline: function (permission) {
        if (permission == null || permission == undefined) {
            return "";
        }
        return permission.replace(/:/g, "_");
    },
    handlerMenuFun: function (permission) {
        var fun = this.convertUnderline(permission);
        try {
            if (fun != undefined && fun != "") {
                eval(fun).apply(this, [fun]);
            }
        } catch (e) {
        }
    }
};
/**
 * Demo演示
 */
function demo_list(id) {
    $("#" + id).text("(12)");
}

/*function diabetes_followplan_followplanlist(id) {
    $.ajax({
        url: ctx + "/diabetes/followplan/getPlanCounts",
        type: "post",
        success: function (data) {
            $("#" + id).text("(" + data + ")");
        }
    })
}

function doctor_followplan_followplanlist(id) {
    $.ajax({
        url: ctx + "/doctor/followplan/getPlanCounts",
        type: "post",
        success: function (data) {
            $("#" + id).text("(" + data + ")");
        }
    })
}

//家庭医生--待办--任务
function doctor_task_tasklist(id) {
    $.ajax({
        url: ctx + "/doctor/task/getTaskCounts",
        type: "post",
        success: function (data) {
            $("#" + id).text("(" + data + ")");
        }
    })
}
//家庭医生--待办--干预
function doctor_intervene_intervenelist(id) {
    $.ajax({
        url: ctx + "/doctor/intervene/getInterveneCounts",
        type: "post",
        success: function (data) {
            $("#" + id).text("(" + data + ")");
        }
    })
}
//家庭医生--待办--未分配任务
function doctor_task_waitTask(id) {
    $.ajax({
        url: ctx + "/doctor/team/getRwjgCounts",
        type: "post",
        success: function (data) {
            $("#" + id).text("(" + data + ")");
        }
    })
}

//家庭医生--待办--地址完善
function doctor_task_finishAddress(id) {

    $.ajax({
        url: ctx + "/doctor/task/getAddressCounts",
        type: "post",
        success: function (data) {
            $("#" + id).text("(" + data + ")");
        }
    })
}*/
