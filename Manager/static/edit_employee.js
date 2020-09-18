var condition = 0;
function onDelete(){
    answer = confirm("Do you want to delete this employee?")
    if (answer == true){
        condition = 1;
    }
    else{
        condition = 2;
    }
}
function checkDelete(){
    if (condition == 0){
        return true;
    }
    else if(condition == 1){
        return true;
    }
    else{
        return false;
    }
}