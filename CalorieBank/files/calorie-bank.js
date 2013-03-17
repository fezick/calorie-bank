$(document).ready(function(){
    $("td.calorie_report button.cancel").click(function(){
        // Capture row id and cancel the edit form
        row_id = $(this).attr("data-parent-id");
        close_row_form(row_id);
    })
    $("td.calorie_report .static").click(function(){
        // replace static calorie display with update form
        row_id = $(this).parent()[0].id;
        $("#"+row_id+"_static").hide()
        $("#"+row_id+"_update").show()
        $("#"+row_id+"_update").children("input").focus()
        $("#"+row_id+"_update button").removeClass("disabled");
    });
    $("td.calorie_report .update .save").click(function(){
        // get the new calorie val and call the ajax updater
        row_id = $(this).attr("data-parent-id");
        newcal = $("#"+row_id+" .calorie_report_input").val()
        save(row_id,newcal);
    });
    row_count = 0; // init row counter
    $(".table tr").each(function(){
        /*
        By default, hide all rows beyond 1 week. Also creates a button to 
        display all days.
        To Do: More granular control to handle lots of data.
        */
        console.log(row_count)
        if(row_count>=8){ // show a weeks worth of days and the header row
            $(this).addClass("hidden_row");
            $(this).hide();
        }
        if(row_count==8){
            $(".table").after("<button class='btn btn-info' id='show_all_days'>Show All</button>");
        } 
        row_count++;
    });
});
$("#show_all_days").ready(function(){
    /*
    Handled the click on the dynamic button created in the document ready 
    section.
    */
    $(this).click(function(){
        $("tr.hidden_row").fadeIn(500);
        $("#show_all_days").hide();
    });
});

function close_row_form(row_id){
    /*
    Cancel the editing of calories for a given day

    Inputs:
        :row_id:    the ID of the day being canceled.
    */
    $("#"+row_id+"_static").show()
    $("#"+row_id+"_update").hide()
}
function save(row_id,cals){
    /*
    Calls the ajax to update a day's calories

    Inputs:
        :row_id:    the ID of the day to edit
        :cals:      the new calorie value for the day
    */
    $("#"+row_id+"_update button").addClass("disabled");
    $.ajax({
        url: "/update/",
        data: {"day_id":row_id.replace("day_",""),"calories":cals},
        success: function(data){
            update_row_form(data.row_id,data.cals,data.balance,data.day_bal);
            close_row_form(data.row_id);
        }
    });
}
function update_row_form(row_id,cals,balance,day_bal){
    /*
    Performs the update of a calorie count displau for a given day after
    the ajax returns successful

    Inputs:
        :row_id:    the id of the row being edited
        :cals:      the new calorie count to display
        :balance:   the updated global balance
        :day_bal:   the updated balance of the single day 
    */
    $("#"+row_id+"_static").html(cals);
    $("#"+row_id+"_balance").html(day_bal);
    if(day_bal < 0){
        $("#"+row_id+"_balance").removeClass("label-success")
        $("#"+row_id+"_balance").addClass("label-important")
    }else{ 
        $("#"+row_id+"_balance").removeClass("label-important")
        $("#"+row_id+"_balance").addClass("label-success")
    }
    $("#"+row_id+"_update").children("input").val(cals)
    $("#balance h1").html(balance)
}
