
var dictionaryFromServer = document.getElementById("query").value
var dictionary = JSON.parse(dictionaryFromServer);


   function addElement(){
    var totalForms = document.getElementById("id_form-TOTAL_FORMS").value;
    //forms ids start from 0
    var existing_row_employee = document.getElementById("id_form-0-employee");
    var new_row_employee = existing_row_employee.cloneNode(true);
    new_row_employee.id = "id_form-" + totalForms + "-employee";
    new_row_employee.name = "form-" + totalForms + "-employee";
    var delete_option = document.createElement('option');
    delete_option.appendChild(document.createTextNode("Delete"));
    delete_option.value = "delete";
    new_row_employee.appendChild(delete_option);
    document.getElementById("names").appendChild(new_row_employee);
    
    var existing_row_point = document.getElementById("id_form-0-point");
    var new_row_point = existing_row_point.cloneNode(true);
    new_row_point.id = "id_form-" + totalForms + "-point";
    new_row_point.name = "form-" + totalForms + "-point";
    new_row_point.value = 0;

    document.getElementById("indexes").appendChild(new_row_point);
    
    var existing_row_tip = document.getElementById("id_form-0-tip_amount");
    var new_row_tip = existing_row_tip.cloneNode(true);
    new_row_tip.id = "id_form-" + totalForms + "-tip_amount";
    new_row_tip.name = "form-" + totalForms + "-tip_amount";
    new_row_tip.value = 0;
    document.getElementById("tips").appendChild(new_row_tip);

    var existing_row_paid_today = document.getElementById("id_form-0-paid_today");
    var new_row_paid_today = existing_row_paid_today.cloneNode(true);
    new_row_paid_today.id = "id_form-" + totalForms + "-paid_today";
    new_row_paid_today.name = "form-" + totalForms + "-paid_today";
    new_row_paid_today.value = 0;
    document.getElementById("paid-todays").appendChild(new_row_paid_today);

    var existing_row_paid_later = document.getElementById("id_form-0-paid_later");
    var new_row_paid_later = existing_row_paid_later.cloneNode(true);
    new_row_paid_later.id = "id_form-" + totalForms + "-paid_later";
    new_row_paid_later.name = "form-" + totalForms + "-paid_later";
    new_row_paid_later.value = 0;

    document.getElementById("paid-laters").appendChild(new_row_paid_later);

    totalForms = parseInt(totalForms) + 1;
    document.getElementById("id_form-TOTAL_FORMS").value = totalForms.toString();
   }
    
    
 function total_cc_tip(){
     var cc_tip = parseFloat(document.getElementById("cc_tip").value);
     var service_charge = parseFloat(document.getElementById("service_charge").value);
     var cc_t_tip = (service_charge + cc_tip).toFixed(2);
     document.getElementById("Total_Tip_By_Cards").value = cc_t_tip;
     document.getElementById("Total_Tip_By_Cards_2").value = cc_t_tip;
 }
function total_cash_sales(){
    var cash_sales = parseFloat(document.getElementById("cash_sales").value);
    var cash_tip = parseFloat(document.getElementById("cash_tip").value);
    var total_cash = (cash_tip + cash_sales).toFixed(2);
     document.getElementById("Total_Cash").value = total_cash;
     document.getElementById("cash_tip_2").value = cash_tip
}
function total_tip(){
   var cc_tips = document.getElementById("Total_Tip_By_Cards_2").value;
   var cash_tip = document.getElementById("cash_tip_2").value;
   document.getElementById("Total_Tip").value = parseInt(cc_tips)+parseInt(cash_tip)
   document.getElementById("Total_Tip_2").value = parseInt(cc_tips)+parseInt(cash_tip)

}
function shift_tip_func(){
    var total_tip = parseFloat(document.getElementById("Total_Tip_2").value);
    var pre_shift_tip = parseFloat(document.getElementById("pre_shift_tip").value);
    var shift_tip = (total_tip-pre_shift_tip).toFixed()
    document.getElementById("shift_tip").value = shift_tip;

}



function getIndexOfEmployee(doc){
    var selectedEmployeeId = doc.value
    index = relativeIndexFinder(doc)
    document.getElementById("indexes").children[index].value = dictionary[selectedEmployeeId]
}
function relativeIndexFinder(doc){
    //finds out which element of the div is changing, returns the index of the element in the children array
    var parentElement = doc.parentNode;
    var index = Array.prototype.indexOf.call(parentElement.children, doc);
    return index
}
function paidLaterCalculator(doc){
    index = relativeIndexFinder(doc);
    var total_tip = parseInt(document.getElementById("tips").children[index].value);
    var paid_today = parseInt(doc.value)
    var paid_later = total_tip-paid_today;
    document.getElementById("paid-laters").children[index].value = paid_later
}
function calculateTotalIndex(){
    var doc = document.getElementById("total_index");
    var sum = 0;
    var indexes = document.getElementById("indexes");
    for (i = 1; i < indexes.children.length; i++){
        sum += parseFloat(indexes.children[i].value);
    }
    doc.value = sum.toFixed(2);
}
function calculateTips(){
    var tips = document.getElementById("tips");
    if (document.getElementById("total_index").value.length == 0){
        alert("Enter the Total Index first. ");
    }
    else if(document.getElementById("shift_tip").value.length == 0){
        alert("Make sure the shift field is entered!");
    }
    else{
    var total_index = parseFloat(document.getElementById("total_index").value).toFixed(2);
    var shift_tip = parseFloat(document.getElementById("shift_tip").value).toFixed(2);
    var singlePoint = shift_tip/total_index;
    var indexes = document.getElementById("indexes");
    for (i = 1; i<tips.children.length; i++){
        var performance_index = indexes.children[i].value;
        if(performance_index.length == 0){
            alert("Enter the employees info and their indexes first");
            return 0;
        }
        tips.children[i].value = parseInt(performance_index * singlePoint);
    }
    calculateTipLeft();
}
}
function calculateTipLeft()
{
    var tips = document.getElementById("tips");
    var sum = 0;
    for (i = 1; i < tips.children.length; i++){
        var value = parseInt(tips.children[i].value);
        sum += value;
    }
    var shift_tip = parseFloat(document.getElementById("shift_tip").value).toFixed(2);
    var tip_left = shift_tip - sum;
    document.getElementById("tip_left").value = tip_left;  
    
}
function validate(){
    
    var elements = document.getElementById("form").elements
    error = 0
    var invalid_ids = [];
    for (element in elements){
        if (elements[element].value===""){
            error += 1;
            invalid_ids.push(elements[element].id);
        }  
    }  
    if (error != 0){
    alert("Not all the fields have been filled");

    for (id in invalid_ids){
        var x = document.getElementById(invalid_ids[id]);
        x.classList.add("Flash")
        x.addEventListener('animationend', function(){
            this.classList.remove("Flash")
        })
        }
        //x.style = "background-color:blue; animation-duration: 1s;"
        return false;
    }
    
    else{
    return true
}
}
function checkToDelete(doc){
    if (doc.value == "delete"){
        var index = relativeIndexFinder(doc)
        var relative_performance_index = document.getElementById("indexes").children[index];
        var relative_tip = document.getElementById("tips").children[index];
        var relative_paid_today = document.getElementById("paid-todays").children[index];
        var relative_paid_later = document.getElementById("paid-laters").children[index];
        doc.remove()
        relative_paid_later.remove()
        relative_paid_today.remove()
        relative_tip.remove()
        relative_performance_index.remove()
        document.getElementById("id_form-TOTAL_FORMS").value -=1;


    }
}
function calculateCashLeft()
{
    var paid_todays = document.getElementById("paid-todays");
    var sum = 0;
    for (i = 1; i < paid_todays.children.length; i++){
        var value = parseInt(paid_todays.children[i].value);
        sum += value;
    }
    var total_cash = parseFloat(document.getElementById("Total_Cash").value).toFixed(2);
    var cash_left = total_cash - sum;
    document.getElementById("cash_left").value = cash_left;  
    
}