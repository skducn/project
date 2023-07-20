$(function () {
    $(".clickLabel").click(function () {
        var readonly = $(this).prop("readonly");
        if (readonly == "readonly") {
            return;
        }
        var index = $(this).attr("index");
        var itemCode = $(this).attr("itemCode");
        var valueIndex = $(this).attr("valueIndex");
        var prefix = $(this).attr("prefix");
        if (prefix == undefined) {
            prefix = "";
        }
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
            $("#checkValue" + prefix + index).val("");
            $("#checkLabel" + prefix + index).val("");
        } else {
            $("#checkValue" + prefix + index).val(itemCode);
            $("#checkLabel" + prefix + index).val(valueIndex);
            $("#checkLabel" + prefix + index).focus();
            $(this).siblings(".selected").removeClass("selected");
            $(this).addClass("selected");
        }
        try {
            var fun = $(this).attr("function");
            if (fun != undefined && fun != "") {
                eval(fun).apply(this, ["#checkLabel" + prefix + index, valueIndex, itemCode]);
            }
        } catch (e) {
        }
    });
    $(".inputLabel").bind('keydown', function (e) {
        var key = e.which;
        if (key == 13) {
            e.preventDefault();
            var nextId = $(this).attr("nextId");
            nextSkip(nextId, $(this).val());
        }
    }).bind('keyup', function (e) {
        var index = $(this).attr("index");
        var value = $(this).val();
        var prefix = $(this).attr("prefix");
        if (prefix == undefined) {
            prefix = "";
        }
        if (isNaN(value)) {
            $(this).val(value.substring(0, value.length - 1));
        } else {
            var itemCode = undefined;
            try {
                var val = parseInt(value);
                var itemSize = parseInt($(this).attr("itemSize"));
                if (val > 0 && val <= itemSize && val.toString() == value) {
                    $("#checkValue" + prefix + index).val($("#itemCode" + prefix + index.toString() + val.toString()).attr("itemCode"));
                    $("#itemCode" + prefix + index.toString() + val.toString()).siblings(".selected").removeClass("selected");
                    $("#itemCode" + prefix + index.toString() + val.toString()).addClass("selected");
                } else {
                    $(this).val(value.substring(0, value.length - 1));
                    $("#checkValue" + prefix + index).val($("#itemCode" + prefix + index.toString() + $(this).val()).attr("itemCode"));
                    $("#itemCode" + prefix + index.toString() + val.toString()).siblings(".selected").removeClass("selected");
                    $("#itemCode" + prefix + index.toString() + val.toString()).addClass("selected");
                }
                itemCode = $("#itemCode" + prefix + index.toString() + val.toString()).attr("itemCode");
            } catch (e) {
                $(this).val(value.substring(0, value.length - 1));
                $("#checkValue" + prefix + index).val($("#itemCode" + prefix + index.toString() + $(this).val()).attr("itemCode"));
            }
        }
        try {
            var fun = $(this).attr("function");
            if (fun != undefined && fun != "") {
                eval(fun).apply(this, ["#checkLabel" + prefix + index, value, itemCode]);
            }
        } catch (e1) {
        }
    }).bind("blur", function () {
        var index = $(this).attr("index");
        var value = $(this).val();
        var prefix = $(this).attr("prefix");
        if (prefix == undefined) {
            prefix = "";
        }
        if ($.trim(value) == "" || isNaN(value)) {
            $(this).val("");
            $("#checkValue" + prefix + index).val("");
            $(this).parent().find("label.selected").removeClass("selected");
        }
    });


    $(".inputBox").bind('keydown', function (e) {
        var key = e.which;
        var index = $(this).attr("index");
        var itemIndex = parseInt($(this).attr("itemIndex"));
        var itemSize = parseInt($(this).attr("itemSize"));
        var prefix = $(this).attr("prefix");
        if (prefix == undefined) {
            prefix = "";
        }
        if (key == 13) {
            e.preventDefault();
            if ($(this).val() == "") {
                var nextId = $(this).attr("nextId");
                nextSkip(nextId, $(this).val());
            } else {
                if (itemIndex > 0 && itemIndex < itemSize) {
                    $(".inputBox" + prefix + index).each(function () {
                        if ($(this).val() == "") {
                            $(this).focus();
                            return false;
                        }
                    });
                    //$("#checkLabel"+prefix+index+(itemIndex+1).toString()).focus().select();
                } else if (itemIndex == itemSize) {
                    var nextId = $(this).attr("nextId");
                    nextSkip(nextId, $(this).val());
                }
            }
        }
    }).bind('keyup', function (e) {
        var index = $(this).attr("index");
        var value = $.trim($(this).val());
        var prefix = $(this).attr("prefix");
        if (prefix == undefined) {
            prefix = "";
        }
        if (value == "" || isNaN(value)) {
            $(this).val(value.substring(0, value.length - 1));
        } else {
            try {
                var val = parseInt(value);
                var itemSize = parseInt($(this).attr("itemSize"));
                if (val > 0 && val <= itemSize && val.toString() == value) {
                    $("#itemCode" + prefix + index.toString() + val.toString()).addClass("selected");
                    var itemCode = $("#itemCode" + prefix + index.toString() + val.toString()).attr("itemCode");
                } else {
                    var tv = value.substring(0, value.length - 1);
                    $(this).val(tv);
                }
            } catch (e) {
                var tv = value.substring(0, value.length - 1);
                $(this).val(tv);
            }
        }
    }).bind('blur', function (e) {
        var index = $(this).attr("index");
        var value = $.trim($(this).val());
        var prefix = $(this).attr("prefix");
        if (prefix == undefined) {
            prefix = "";
        }
        if (value == "" || isNaN(value)) {
            setCheckBox(prefix, index, value);
            // $(this).val(value.substring(0,value.length-1));
        } else {
            try {
                var val = parseInt(value);
                var itemSize = parseInt($(this).attr("itemSize"));
                if (val > 0 && val <= itemSize && val.toString() == value) {
                    setCheckBox(prefix, index, value);
                } else {
                    var tv = value.substring(0, value.length - 1);
                    $(this).val(tv);
                    setCheckBox(prefix, index, tv);
                }
            } catch (e) {
                var tv = value.substring(0, value.length - 1);
                $(this).val(tv);
                setCheckBox(prefix, index, tv);
            }
            $(".inputBox" + prefix + index).each(function () {
                if ($(this).val() == "") {
                    $(this).focus();
                    return false;
                }
            });
        }
        try {
            var itemCode = $("#itemCode" + prefix + index.toString() + value).attr("itemCode");
            var fun = $(this).attr("function");
            if (fun != undefined && fun != "") {
                eval(fun).apply(this, [".clickBox" + prefix + index, value, itemCode]);
            }
        } catch (e) {
        }
    });
    $(".clickBox").click(function () {
        var readonly = $(this).prop("readonly");
        if (readonly == "readonly") {
            return;
        }
        var index = $(this).attr("index");
        var valueIndex = $(this).attr("valueIndex");
        var prefix = $(this).attr("prefix");
        if (prefix == undefined) {
            prefix = "";
        }
        var itemCode = $(this).attr("itemCode");
        if ($(this).hasClass("selected")) {
            setCheckBox(prefix, index, valueIndex, "true");
        } else {
            setCheckBox(prefix, index, valueIndex);
        }
        try {
            var fun = $(this).attr("function");
            if (fun != undefined && fun != "") {
                eval(fun).apply(this, [".clickBox" + prefix + index, valueIndex, itemCode]);
            }
        } catch (e) {
        }
    });

    $(".skipElement").bind('keydown', function (e) {
        var key = e.which;
        if (key == 13) {
            e.preventDefault();
            var nextId = $(this).attr("nextId");
            nextSkip(nextId, $(this).val());
        }
    });
});

function skipElement(preId, thisId, nextId) {
    var event = event ? event : window.event;
    if (event.keyCode == 13) {
        if ($.isPlainObject(nextId)) {
            var value = mini.get(thisId).getValue();
            var nId = nextId[value];
            if (nId != undefined) {
                nextId = nId;
            } else {
                nextId = nextId["other"];
            }
        }
        var element = mini.get(nextId);
        if (element == null || element == undefined) {
            nextSkip(nextId, $("#" + thisId).val());
        } else {
            try {
                if (!mini.get(thisId).isShowPopup()) { //判断当前的miniui组件下拉框是下拉显示
                    element.focus();
                    if (element.type == "combobox" || element.type == "datepicker") {
                        element.showPopup();
                        //element.select(0);
                    }
                }
            } catch (e) {
                element.focus();
                if (element.type == "combobox" || element.type == "datepicker") {
                    element.showPopup();
                    //element.select(0);
                }
            }
        }
    }
}

function exArray(arr, v) {
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == v) {
            return true;
        }
    }
    return false;
}
/**
 * 调整到下一个
 * @param nextId 下一个输入框
 * @param value 当前输入框中的值
 */
function nextSkip(nextId, value) {
    if (nextId == undefined) {
        return;
    }
    if ($.type(nextId) == "string" && nextId.indexOf("'") >= 0) {
        nextId = $.parseJSON(nextId.replace(new RegExp(/'/g), "\""));
    }
    if (value != undefined && value != null && $.isPlainObject(nextId)) {
        var nId = nextId[value];
        if (nId != undefined) {
            nextSkip(nId);
        } else {
            nextSkip(nextId["other"]);
        }
    } else {
        var el = mini.get(nextId);
        if (el != null && el != undefined) {
            el.focus();
            if (el.type == "combobox" || el.type == "datepicker") {
                el.showPopup();
            }
        } else if ($("#" + nextId).length == 0) {
            if ($("input[id^='" + nextId + "']").length > 0) {
                $($("input[id^='" + nextId + "']").get(0)).focus().select();
            } else if ($("input[id^='checkLabel" + nextId + "']").length > 0) {
                $($("input[id^='checkLabel" + nextId + "']").get(0)).focus().select();
            }
        } else if ($("#" + nextId).is("select")) {
            $("#" + nextId).select2("open");
            $("#select2-drop").find(":text").focus();
        } else {
            $("#" + nextId).focus().select();
        }
    }
}
/**
 * @param index
 * @param value
 * @param unSelected
 *            是否选中或者取消选中
 * @returns {Boolean}
 */
function setCheckBoxEmpty(prefix, index, value, unSelected) {
    var itemValue = $("#itemCode" + prefix + index + value).attr("itemValue");
    if (itemValue == "无" || itemValue == "不确定" || itemValue == "无相关临床症状" || itemValue == "以上情况均无") {
        $(".inputBox" + prefix + index).each(function () {
            $(this).val("");
        });
        var item = $("#itemCode" + prefix + index.toString() + value);
        item.siblings(".selected").removeClass("selected");
        var code = item.attr("itemCode");
        if (unSelected == "true") {
            $("#checkValue" + prefix + index).val("");
            item.removeClass("selected");
        } else {
            $($(".inputBox" + prefix + index).get(0)).val(value);
            $("#checkValue" + prefix + index).val(code);
            item.addClass("selected");
        }
        //$($(".inputBox"+prefix+index).get(1)).focus();
        return true;
    } else {
        $(".inputBox" + prefix + index).each(function () {
            var itemValue = $("#itemCode" + prefix + index + $(this).val()).attr("itemValue");
            if (itemValue == "无" || itemValue == "不确定" || itemValue == "无相关临床症状" || itemValue == "以上情况均无") {
                $(this).val("");
            }
        });
    }
    return false;
}
function setCheckBox(prefix, index, value, unSelected) {
    if (setCheckBoxEmpty(prefix, index, value, unSelected)) {
        return;
    }
    var boxes = $(".inputBox" + prefix + index);
    var arr = new Array();
    var flag = true;
    var j = 0;
    if (unSelected != "true" && value != "" && !isNaN(value)) {
        arr[j++] = parseInt(value);
    }
    var radioValues = $("#checkValue" + prefix + index).attr("radioValues");
    var radioArr = undefined;
    var radioFlag = false;
    if (radioValues != undefined) {
        radioArr = radioValues.split(",");
    }
    if (radioArr != undefined && exArray(radioArr, value)) {
        radioFlag = true;
    }
    for (var i = 0; i < boxes.length; i++) {
        var val = $.trim($(boxes.get(i)).val());
        if (setCheckBoxEmpty(prefix, index, val, unSelected)) {
            return;
        }
        if (val != "" && !isNaN(val)) {
            var v = parseInt(val);
            if (radioArr != undefined && radioFlag) {
                if (exArray(radioArr, val)) {
                    continue;
                }
            }
            if (unSelected == "true" && val == value) {
                continue;
            }
            if (!exArray(arr, v)) {
                arr[j++] = v;
            }
        }
    }
    if (arr.length > 0) {
        arr.sort(function (a, b) {
            return a > b ? 1 : -1
        });
    }
    $(".clickBox" + prefix + index).removeClass("selected");
    var checkValue = "";
    for (var i = 0; i < boxes.length; i++) {
        if (i < arr.length) {
            var code = $("#itemCode" + prefix + index.toString() + arr[i].toString()).attr("itemCode");
            $("#itemCode" + prefix + index.toString() + arr[i].toString()).addClass("selected");
            if (checkValue != "") {
                checkValue += ",";
            }
            checkValue += code;
            $(boxes.get(i)).val(arr[i]);
        } else {
            $(boxes.get(i)).val("");
        }
    }
    $("#checkValue" + prefix + index).val(checkValue);
}
function setCheckBoxInput(cssClass, value) {
    $("." + cssClass).each(function () {
        var val = $.trim($(this).val());
        if (val == "") {
            $(this).val(value);
            return false;
        } else if (value == val) {
            return false;
        }
    });
}

/**
 * 设置checkbox多选框中的值
 * @param name
 * @param value
 */
function setCheckBoxsView(name, value) {
    $("input[name='" + name + "']").val(value);
    var index = $("input[name='" + name + "']").attr("index");
    var prefix = name.replace('.', '_');
    var arr = value.split(',');
    var xx = 0;
    $(".inputBox" + prefix + index).val("");
    $(".clickBox" + prefix + index).each(function () {
        var label = $(this);
        var v1 = label.attr("itemCode");
        var vi = label.attr("valueIndex");
        if(arrHas(arr,v1)) {
            label.addClass("selected");
            $($(".inputBox" + prefix + index).get(xx++)).val(vi);
        } else {
            label.removeClass("selected");
        }
    });
}

function addCheckBoxsView(name,value){
    var val = $("input[name='" + name + "']").attr("value");
        var arr = val.split(',');
        if(!arrHas(arr,value)){
            arr.push(value);
        }
        setCheckBoxsView(name,arr.join(","));
}

function clearCheckBoxValueByValue(name,value){
    var val = $("input[name='" + name + "']").attr("value");
    if(val != undefined && val != "") {
        var arr = val.split(',');
        var vals = [];
        for(var i = 0 ;i < arr.length;i++){
            if(arr[i] != value){
                vals.push(arr[i]);
            }
        }
        setCheckBoxsView(name,vals.join(","));
    }
}

function arrHas(arr,value){
    if(arr == null || arr == undefined || arr.length == 0) {
        return false;
    }
    for(var i = 0 ;i<arr.length;i++){
        if(arr[i] == value) {
            return true;
        }
    }
    return false;
}

function setRadiosView(name, value) {
    $("input[name='" + name + "']").val(value);
    var index = $("input[name='" + name + "']").attr("index");
    var prefix = name.replace('.', '_');
    $("#checkLabel" + prefix + index).val("");
    $(".clickLabel" + prefix + index).each(function () {
        var label = $(this);
        var v1 = label.attr("itemCode");
        var vi = label.attr("valueIndex");
        if (v1 == value) {
            label.addClass("selected");
            $("#checkLabel" + prefix + index).val(vi);
        } else {
            label.removeClass("selected");
        }
    });
}

function clearRadioValue(name) {
    var input = $("input[name='" + name + "']");
    var index = input.attr("index");
    var prefix = convertUnderline(name);
    $("#checkLabel" + prefix + index).val("");
    $(".clickLabel" + prefix + index).removeClass("selected");
    $("input[name='" + name + "']").val("");
}
function clearCheckBoxValue(name) {
    var input = $("input[name='" + name + "']");
    var index = input.attr("index");
    var prefix = convertUnderline(name);
    $("input[name='" + name + "']").val("");
    $(".clickBox" + prefix + index).removeClass("selected");
    $(".inputBox" + prefix + index).val("");

}
function setCheckBoxInputs(cssClass, values) {
    var arr = values.split(',');
    $.each(arr, function (i, v) {
        setCheckBoxInput(cssClass, v);
    });
}
function setCheckBoxReadonly(name) {
    var input = $("input[name='" + name + "']");
    var index = input.attr("index");
    var prefix = convertUnderline(name);
    $(".inputBox" + prefix + index).prop("readonly", "readonly");
    $(".clickBox" + prefix + index).prop("readonly", "readonly");
    $(".inputBox" + prefix + index).attr("disabled", "disabled");
    $(".clickBox" + prefix + index).attr("disabled", "disabled");
}
function clearCheckBoxReadonly(name) {
    var input = $("input[name='" + name + "']");
    var index = input.attr("index");
    var prefix = convertUnderline(name);
    $(".inputBox" + prefix + index).removeProp("readonly");
    $(".clickBox" + prefix + index).removeProp("readonly");
    $(".inputBox" + prefix + index).removeAttr("disabled");
    $(".clickBox" + prefix + index).removeAttr("disabled");
}

function setRadioReadonly(name) {
    var input = $("input[name='" + name + "']");
    var index = input.attr("index");
    var prefix = convertUnderline(name);
    $("input[name='radioName" + prefix + index + "']").prop("readonly", "readonly");
    $(".clickLabel" + prefix + index).prop("readonly", "readonly");
    $("input[name='radioName" + prefix + index + "']").attr("disabled", "disabled");
    $(".clickLabel" + prefix + index).attr("disabled", "disabled");
}
function clearRadioReadonly(name) {
    var input = $("input[name='" + name + "']");
    var index = input.attr("index");
    var prefix = convertUnderline(name);
    $("input[name='radioName" + prefix + index + "']").removeProp("readonly");
    $(".clickLabel" + prefix + index).removeProp("readonly");
    $("input[name='radioName" + prefix + index + "']").removeAttr("disabled");
    $(".clickLabel" + prefix + index).removeAttr("disabled");
}
function convertUnderline(str) {
    if (str == null || str == undefined) {
        return "";
    }
    return str.replace(".", "_").replace(/:/g, "_");
}

function setAllReadOnly(flag){
    if(flag==true){
        $(".clickBox").prop("readonly","readonly");
        $(".inputBox").prop("readonly","readonly");
        $(".clickLabel").prop("readonly","readonly");
        $(".inputLabel").prop("readonly","readonly");
    }else {
        $(".clickBox").removeProp("readonly");
        $(".inputBox").removeProp("readonly");
        $(".clickLabel").removeProp("readonly");
        $(".inputLabel").removeProp("readonly");
    }

}





