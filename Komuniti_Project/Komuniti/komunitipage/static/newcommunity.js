$('#com_name').keypress(function (event) {
    //event.preventDefault(); // preventing submition

    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13') {
        event.preventDefault(); // preventing submition

        jQuery.ajax({
            type: "POST", url: "/tags",
            data: {"query": $('#com_name').val()},
            success:
                function (result) {
                    tagValue = "";
                    console.log(result);
                    if (result.results !== undefined) {
                        if (result.results.bindings !== undefined && result.results.bindings.length > 0) {
                            var tag_cnt = 0;
                            for (var i = 0; i < result.results.bindings.length; i++) {
                                if (result.results.bindings[i].itemDescription !== undefined) {
                                    if (!result.results.bindings[i].itemDescription.value.includes("disambiguation")
                                        || result.results.bindings[i].itemDescription.value !== "") {
                                        tagValue = result.results.bindings[i].itemDescription.value
                                        $('#com_tags').tagsinput('add', tagValue);

                                        // var obj = JSON.parse(tagsJson);
                                        // obj['theTags'].push({
                                        //     "tag": tagValue
                                        // });
                                        // tagsJson = JSON.stringify(obj);
                                    }
                                }
                            }
                        }
                    }
                }
        });
    }
});
$("#addCommunity").on("click", function () {
    var tagList = $('#com_tags').tagsinput('items');

    for (var i = 0; i < tagList.length; i++) {
        var obj = JSON.parse(tagsJson);
        obj['theTags'].push({
            "tag": tagList[i]
        });
        tagsJson = JSON.stringify(obj);
    }
    $("#communityTags").val(tagsJson);

});
