function refresh_botlist(){
    $("#botList tbody tr").remove();
    var botTable = document.getElementById("botList").getElementsByTagName('tbody')[0];
    
    $.getJSON("/refresh_botlist", function(data){
        $.each(data, function(key, val){
            console.log(key, val);
            var row = botTable.insertRow(0);

            var query = val.split('|')[2]
            row.id = key;
            $('#'+key).data('bokehName', {'bokehName': query});

            var bokehname = $('#'+key).data('bokehName');
            console.log(bokehname);

            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);

            var view_btn = document.createElement('input');
            view_btn.type = "button";
            view_btn.className = "btn";
            view_btn.value = "View Chart";
            view_btn.onclick = function() {
                location.assign(`/view/${query}`);
            }

            var del_btn = document.createElement('input');
            del_btn.type = "button";
            del_btn.className = "btn";
            del_btn.value = "Delete Bot";
            del_btn.addEventListener('click', function(){
                delete_bot(key);
            });

            cell1.innerHTML = key;
            cell2.innerHTML = val;
            cell3.appendChild(view_btn);
            cell4.appendChild(del_btn);
        });
    });
}

function delete_bot(bot_id){
    console.log(bot_id);
    const url =  `/delete_bot/${bot_id}`
    console.log(url)
    $.ajax({
        url: url,
        type: 'DELETE',
        success: function(result) {
            console.log(result)
            $(`#${bot_id}`).remove();
        }
    });
}



$(function(){
    console.log("Performing dom manipulations")
    refresh_botlist();
    $("#refresh_botlist_btn").click(refresh_botlist);
    
});
