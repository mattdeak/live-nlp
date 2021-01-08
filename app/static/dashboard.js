function refresh_botlist(){
    $("#botList tbody tr").remove();
    var botTable = document.getElementById("botList").getElementsByTagName('tbody')[0];
    
    $.getJSON("/refresh_botlist", function(data){
        $.each(data, function(key, val){
            console.log(key, val);
            var row = botTable.insertRow(0);

            var split = val.split('|')

            var source = split[0]
            var analyzer = split[1]
            var query = split[2]
            row.id = key;
            $('#'+key).data('bokehName', {'bokehName': query});

            var bokehname = $('#'+key).data('bokehName');
            console.log(bokehname);

            var id_cell = row.insertCell(0);
            var source_cell = row.insertCell(1);
            var analysis_type_cell = row.insertCell(2);
            var analyzer_cell = row.insertCell(3);
            var query_cell = row.insertCell(4)
            var initalization_cell = row.insertCell(5);


            id_cell.innerHTML = key;
            source_cell.innerHTML = source;
            analysis_type_cell.innerHTML = 'Live'; //TODO: Automate
            analyzer_cell.innerHTML = analyzer;
            query_cell.innerHTML = query;
            initalization_cell.innerHTML = 'NotImplemented'
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
