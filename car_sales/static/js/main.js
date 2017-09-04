$(document).ready(
    $(function() {

        // jQuery selection for the 2 select boxes
        var dropdown = {
            make: $('#make'),
            model: $('#model')
        };

        // call to update on load
        updateModels(true);

        // function to call XHR and update county dropdown
        function updateModels(onPageLoad) {
            var send = {
                make: dropdown.make.val()
            };
            dropdown.model.attr('disabled', 'disabled');
            dropdown.model.empty();
            if(onPageLoad === false){
            $.ajax({
                 url:'/stock/return_models/'+send.make,
                 success: function(data) {
                    data.forEach(function(item) {
                        dropdown.model.append(
                        $('<option>', {
                            value: item[0],
                            text: item[1]
                        })
                    );
                    dropdown.model.removeAttr('disabled');
                 })},
                 failure: function(response){
                    console.log("Failure");
                 }
            })}
            var make_id = dropdown.make.val();
            };

        // event listener to make dropdown change
        dropdown.make.on('change', function() {
            updateModels(false);
        });

        function getSearchTerms() {
            return {
                max_price: $('#max_price').val(),
                min_price: $('#min_price').val(),
                make_id: $('#make').val(),
                model_id: $('#model').val()
            }

        };

        function searchStock() {
            var searchTerms = getSearchTerms();
            console.log(searchTerms);
            $.ajax({
                url:'/home',
                success: function(data) {
                    console.log("Success");
                },
                failure: function(response){
                    console.log("Failure");
                }
            })
        };

    })
);
